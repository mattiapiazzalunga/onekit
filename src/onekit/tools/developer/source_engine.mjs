// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Source processing rules. Engine loading and process isolation belong to callers.
export const parsers={javascript:'babel',typescript:'typescript',jsx:'babel',tsx:'typescript',html:'html',css:'css',scss:'scss',less:'less',json5:'json5',jsonc:'json',yaml:'yaml',markdown:'markdown',mdx:'mdx',graphql:'graphql',vue:'vue',svelte:'svelte',astro:'astro',solidity:'antlr',php:'php'};
export const pluginPackages={svelte:'prettier-plugin-svelte',astro:'prettier-plugin-astro',solidity:'prettier-plugin-solidity',php:'@prettier/plugin-php'};
export const minifierLanguages=new Set(['javascript','typescript','jsx','tsx','css','html','svg','graphql']);
// Native formatter hosts implement this small interface without exposing their
// process, library or filesystem management to the source processing rules.
export const formatterExtensions={python:'py',java:'java',c:'c',cpp:'cpp',csharp:'cs',go:'go',dart:'dart',lua:'lua',bash:'bash',shell:'sh',sql:'sql',hcl:'hcl',terraform:'tf'};

export async function transformSource({operation,language,text},{load,plugins=async()=>[],nativeFormat,nativeValidate}){
  if(typeof text!=='string')throw new Error('Source text must be a string.');
  let result;
  if(operation==='minify'){
    if(['javascript','typescript','jsx','tsx','css'].includes(language))result=(await (await load('esbuild')).transform(text,{minify:true,loader:({javascript:'js',typescript:'ts'})[language]||language})).code;
    else if(language==='html')result=await (await load('html-minifier-terser')).minify(text,{collapseWhitespace:true,conservativeCollapse:true,removeComments:true,minifyJS:false,minifyCSS:false});
    else if(language==='svg'){
      if(/<!DOCTYPE|<!ENTITY/i.test(text))throw new Error('DTD and entity declarations are disabled.');
      result=(await load('svgo')).optimize(text).data;
    }else if(language==='graphql')result=(await load('graphql')).stripIgnoredCharacters(text);
  }else if(operation==='format'||operation==='validate'){
    if(operation==='validate'&&nativeValidate){
      await nativeValidate(text,{language});
      return text;
    }
    const parser=parsers[language];
    if(!parser&&nativeFormat&&formatterExtensions[language]){
      result=await nativeFormat(text,{language,filename:`input.${formatterExtensions[language]}`,
        settings:{},...(['c','cpp','csharp','java'].includes(language)?{style:'LLVM'}:{}),...(language==='sql'?{dialect:'sql'}:{})});
    }else{
    if(!parser)throw new Error('No source parser is registered for this language.');
    result=await (await load('prettier')).format(text,{parser,plugins:await plugins(language),...(language==='php'?{phpVersion:'8.5'}:{})});
    }
  }
  if(typeof result!=='string')throw new Error('No source engine is registered for this operation.');
  return result;
}

export function assertSyntaxTree(root,{maxNodes=Infinity,maxDepth=Infinity,namedOnly=false}={}){
  const nodes=[{node:root,depth:0}];let visited=0;
  while(nodes.length){
    const {node,depth}=nodes.pop();
    if(++visited>maxNodes||depth>maxDepth)throw new Error('Source is too complex. Split it into smaller files.');
    if(node.isMissing||node.type==='ERROR'){
      const location=node.startPosition||{row:0,column:0};
      throw new Error(`Syntax error at line ${location.row+1}, column ${location.column+1}: ${node.isMissing?'missing '+node.type:String(node.text).slice(0,120)}`);
    }
    const children=namedOnly?node.namedChildren:node.children;
    for(let index=children.length-1;index>=0;index--)nodes.push({node:children[index],depth:depth+1});
  }
  if(root.hasError)throw new Error('The source contains a syntax error.');
}

export function validateLocalReferences(document,{maxReferences=Infinity}={}){
  const stack=[document],seen=new Set();let references=0;
  while(stack.length){
    const value=stack.pop();
    if(!value||typeof value!=='object')continue;
    if(seen.has(value))throw new Error('Cyclic or repeated document objects are unsupported.');
    seen.add(value);
    if(Object.hasOwn(value,'$ref')){
      if(++references>maxReferences)throw new Error('Too many document references.');
      if(typeof value.$ref!=='string'||value.$ref[0]!=='#')throw new Error('Only references inside this document are supported.');
      let pointer;
      try{pointer=decodeURIComponent(value.$ref.substring(1));}catch{throw new Error('Invalid JSON Pointer encoding.');}
      if(pointer&&!pointer.startsWith('/'))throw new Error('Expected a local JSON Pointer reference.');
      let resolved=document;
      for(const token of pointer?pointer.substring(1).split('/'):[]){
        if(/~(?:[^01]|$)/.test(token))throw new Error('Invalid JSON Pointer escape.');
        const key=token.replace(/~[01]/g,match=>match==='~0'?'~':'/');
        if(resolved===null||typeof resolved!=='object'||!Object.hasOwn(resolved,key))throw new Error('Unresolved reference: '+value.$ref);
        resolved=resolved[key];
      }
    }
    stack.push(...Object.values(value));
  }
}

export function apiSpecification(value,family){
  if(value===null||typeof value!=='object'||Array.isArray(value))throw new Error('The specification must be an object.');
  if(family==='openapi'){
    if(value.swagger==='2.0')return {family,version:'2.0'};
    const match=/^(3\.[01])\.\d+(?:-.+)?$/.exec(value.openapi||'');
    if(match)return {family,version:match[1]};
    throw new Error('Supported OpenAPI versions: Swagger 2.0, OpenAPI 3.0.x and 3.1.x.');
  }
  if(family==='asyncapi'&&/^(?:2\.[0-6]\.0|3\.[01]\.0)$/.test(value.asyncapi||''))return {family,version:value.asyncapi};
  throw new Error('Unsupported AsyncAPI specification version.');
}

export async function validateAPISpecification(value,{family,schema,maxReferences}={}){
  const specification=apiSpecification(value,family);
  validateLocalReferences(value,{maxReferences});
  const validator=await schema(specification);
  if(!validator(value))throw new Error((validator.errors||[]).slice(0,5).map(error=>`${error.instancePath||'/'} ${error.message}`).join('; '));
}

export function transformContainerRecipe(text,{operation='format',parse,keywords}={}){
  const instructions=parse(text).getInstructions(),allowed=new Set(keywords),edits=[];
  let stages=0;
  for(const instruction of instructions){
    const keyword=instruction.getKeyword().toUpperCase();
    const content=instruction.getArgumentsContent()?.trim();
    if(!allowed.has(keyword))throw new Error('Unknown Dockerfile instruction: '+keyword);
    if(!content)throw new Error(keyword+' requires arguments.');
    if(keyword==='FROM'){
      const args=instruction.getArguments().map(argument=>argument.getValue());
      if(args.length!==1&&(args.length!==3||args[1].toUpperCase()!=='AS'||!/^[-\w.]+$/.test(args[2])))throw new Error('FROM requires an image and an optional AS stage name.');
      stages++;
    }else if(stages===0&&keyword!=='ARG')throw new Error('Only ARG is valid before the first FROM.');
    if(content[0]==='['&&['ADD','COPY','CMD','ENTRYPOINT','RUN','SHELL','VOLUME'].includes(keyword)){
      let argumentsList;
      try{argumentsList=JSON.parse(content);}catch{throw new Error('Invalid JSON arguments for '+keyword);}
      if(!Array.isArray(argumentsList)||argumentsList.length===0||argumentsList.some(argument=>typeof argument!=='string'))throw new Error(keyword+' requires an array of strings.');
    }
    const range=instruction.getInstructionRange();
    if(range.start.line===range.end.line)edits.push({range,keyword});
  }
  if(stages===0)throw new Error('A Dockerfile needs a FROM instruction.');
  if(operation==='validate')return text;
  const lines=text.replace(/\r\n?/g,'\n').split('\n');
  for(const {range,keyword} of edits.reverse()){
    const line=lines[range.start.line];
    lines[range.start.line]=line.substring(0,range.start.character)+keyword+line.substring(range.end.character);
  }
  return lines.join('\n').replace(/\n*$/,'\n');
}

export async function sourceResult(tool,file,process,{scope='parser or configured project checks'}={}){
  const text=new TextDecoder('utf-8',{fatal:true}).decode(file.data);
  if(/[\x00-\x08\x0b\x0e-\x1f\x7f]/.test(text))throw new Error('Binary content is not accepted by this text tool.');
  const match=/^dev-(format|validate|minify)-(.+)$/.exec(tool.id);
  if(!match)throw new Error('Unknown source operation.');
  const [,operation,language]=match;
  let result,details={},warnings=[];
  if(operation==='validate'){
    details={valid:true,language,scope};
    try{await process(text);}catch(error){if(error.setupFailure)throw error;details.valid=false;details.errors=[String(error.message||error).slice(0,2000)];}
    result=JSON.stringify(details,null,2);
  }else result=await process(text);
  if(typeof result!=='string')throw new Error('The engine produced no output.');
  const base=file.name.replaceAll('\\','/').split('/').at(-1).replace(/\.[^.]+$/,'');
  const name=operation==='validate'?`${base}.validation.json`:operation==='minify'&&['typescript','jsx','tsx'].includes(language)?`${base}.js`:file.name;
  if(tool.fidelity==='compromise')warnings.push(tool.note);
  return {files:[{name,data:new TextEncoder().encode(result)}],warnings,details};
}
