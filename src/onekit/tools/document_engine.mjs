// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Portable semantic document conversion. Parsers and raster/PDF writers are host services.
const node=(t,c)=>c===undefined?{t}:{t,c};
const ignored=new Set(['script','style','iframe','object','embed','head','template']);
const containers=new Set(['html','body','main','article','section','header','footer','div','table','thead','tbody','tfoot']);
const structural=new Set([...containers,'p','blockquote','pre','ul','ol','li','tr','hr','h1','h2','h3','h4','h5','h6']);
const children=element=>element.childNodes||[];
const attribute=(element,name)=>(element.attrs||[]).find(value=>value.name===name)?.value||'';
const plain=element=>element.nodeName==='#text'?element.value:children(element).filter(child=>!ignored.has(child.tagName)).map(plain).join('');

export function readHTMLDocument(root,{maxNodes=100000,maxDepth=128,maxBlocks=10000}={}){
  const pending=[[root,0]],warnings=new Set();let count=0,blockCount=0;
  while(pending.length){
    const [element,depth]=pending.pop();
    if(++count>maxNodes||depth>maxDepth)throw new Error('Document is too complex; reduce nesting or split it.');
    for(const child of children(element))pending.push([child,depth+1]);
  }
  function inline(element){
    const tag=element.tagName;
    if(ignored.has(tag)){warnings.add('Active content is omitted.');return [];}
    if(element.nodeName==='#text')return [node('Str',element.value)];
    if(tag==='br')return [node('LineBreak')];
    if(tag==='img'){
      warnings.add('Images are represented by their alternative text; remote images are not fetched.');
      return [node('Str',attribute(element,'alt')||'[image]')];
    }
    if(tag==='ul'||tag==='ol'||tag==='table')return [];
    const content=children(element).flatMap(inline);
    if(tag==='strong'||tag==='b')return [node('Strong',content)];
    if(tag==='em'||tag==='i')return [node('Emph',content)];
    if(tag==='code')return [node('Code',[['',[],[]],plain(element)])];
    if(tag==='a'){
      const url=attribute(element,'href');
      if(/^(https?:|mailto:)/i.test(url)&&!/[\s\x00-\x1f{}\\]/.test(url))return [node('Link',[['',[],[]],content,[url,'']])];
      if(url)warnings.add('Unsupported links are represented by their text.');
    }
    if(tag==='td'||tag==='th')content.push(node('Str',' | '));
    return content;
  }
  const add=(blocks,block)=>{
    if(++blockCount>maxBlocks)throw new Error('Document has too many text blocks.');
    blocks.push(block);
  };
  function blocks(elements){
    const result=[];let runs=[];
    const flush=()=>{
      if(runs.some(run=>run.t!=='Str'||run.c.trim()))add(result,node('Para',runs));
      runs=[];
    };
    for(const element of elements){
      const tag=element.tagName;
      if(ignored.has(tag)){inline(element);continue;}
      if(!structural.has(tag)){runs.push(...inline(element));continue;}
      flush();
      if(/^h[1-6]$/.test(tag))add(result,node('Header',[Number(tag[1]),['',[],[]],children(element).flatMap(inline)]));
      else if(tag==='pre')add(result,node('CodeBlock',[['',[],[]],plain(element)]));
      else if(tag==='hr')add(result,node('HorizontalRule'));
      else if(tag==='ul'||tag==='ol'){
        const items=children(element).filter(child=>child.tagName==='li').map(child=>blocks(children(child)));
        add(result,tag==='ul'?node('BulletList',items):node('OrderedList',[[Number(attribute(element,'start'))||1,{t:'Decimal'},{t:'Period'}],items]));
      }else if(tag==='blockquote')add(result,node('BlockQuote',blocks(children(element))));
      else if(tag==='p'||tag==='li')add(result,node('Para',children(element).flatMap(inline)));
      else if(tag==='tr'){
        warnings.add('Tables are represented by text rows.');
        add(result,node('Para',children(element).flatMap(inline)));
      }else result.push(...blocks(children(element)));
    }
    flush();return result;
  }
  return {document:{'pandoc-api-version':[1,23,1],meta:{},blocks:blocks(children(root))},warnings:[...warnings]};
}

export function escapeLaTeX(value){
  const escapes={'\\':'\\textbackslash{}','~':'\\textasciitilde{}','^':'\\textasciicircum{}'};
  return value.replace(/[\\{}#$%&_~^]/g,character=>escapes[character]||'\\'+character);
}

export function documentLaTeX(document){
  const inline=values=>values.map(value=>{
    if(value.t==='Str')return escapeLaTeX(value.c.replace(/\s+/g,' '));
    if(value.t==='LineBreak')return '\\\\\n';
    if(value.t==='Code')return '\\texttt{'+escapeLaTeX(value.c[1])+'}';
    if(value.t==='Strong'||value.t==='Emph')return '\\'+(value.t==='Strong'?'textbf':'emph')+'{'+inline(value.c)+'}';
    if(value.t==='Link')return '\\href{'+escapeLaTeX(value.c[2][0])+'}{'+inline(value.c[1])+'}';
    return '';
  }).join('');
  function write(blocks,depth=0){
    return blocks.map(block=>{
      switch(block.t){
        case 'Para':return inline(block.c).trim()+'\n';
        case 'Header':return '\\'+['section','subsection','subsubsection','paragraph','subparagraph','subparagraph'][block.c[0]-1]+'*{'+inline(block.c[2]).trim()+'}';
        case 'CodeBlock':return '\\par\\begingroup\\ttfamily\\obeyspaces\n'+escapeLaTeX(block.c[1]).replace(/\n/g,'\\\\\n')+'\n\\par\\endgroup';
        case 'BlockQuote':return '\\begin{quote}\n'+write(block.c,depth)+'\n\\end{quote}';
        case 'HorizontalRule':return '\\par\\noindent\\rule{\\linewidth}{0.4pt}';
        case 'BulletList':case 'OrderedList':{
          const items=block.t==='BulletList'?block.c:block.c[1],environment=block.t==='BulletList'?'itemize':'enumerate';
          const body=items.map(item=>'\\item '+write(item,depth+1)).join('\n');
          return depth>=4?items.map(item=>write(item,depth)).join('\n'):'\\begin{'+environment+'}\n'+body+'\n\\end{'+environment+'}';
        }
        default:throw new Error('Unsupported document block: '+block.t);
      }
    }).join('\n');
  }
  return '\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{hyperref}\n\\begin{document}\n'+write(document.blocks)+'\n\\end{document}\n';
}

export async function convertDocument({text,source,target},{markdown,html,pdf,limits}={}){
  if(typeof text!=='string'||!['md','html'].includes(source)||!['latex','pdf'].includes(target))throw new Error('Unsupported document conversion.');
  const rendered=source==='md'?await markdown(text,{html:false,linkify:false,typographer:false}):text;
  const model=readHTMLDocument(await html(rendered),limits);
  if(target==='latex')return {data:new TextEncoder().encode(documentLaTeX(model.document)),warnings:model.warnings,details:{}};
  const result=await pdf(model.document);
  return {...result,warnings:[...model.warnings,...(result.warnings||[])]};
}
