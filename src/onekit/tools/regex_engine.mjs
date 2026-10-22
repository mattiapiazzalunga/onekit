// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// ECMAScript processing engine for the Node-backed CLI.
const MAX_TEXT=128*1024,MAX_OUTPUT=1024*1024;
function substitute(template,match,input){
  return template.replace(/\$(\$|&|`|'|[0-9]{1,2}|<[^>]*>)/g,(token,key)=>{
    if(key==='$')return '$';if(key==='&')return match[0];if(key==='`')return input.slice(0,match.index);if(key==="'")return input.slice(match.index+match[0].length);
    if(key.startsWith('<'))return match.groups?match.groups[key.slice(1,-1)]??'':token;
    const number=Number(key);if(number>0&&number<match.length)return match[number]??'';
    if(key.length===2&&Number(key[0])>0&&Number(key[0])<match.length)return (match[Number(key[0])]??'')+key[1];
    return token;
  });
}
export function testRegex(input,options={}){
  if(typeof input!=='string'||new TextEncoder().encode(input).length>MAX_TEXT)throw new Error('Test text must contain at most 128 KiB of UTF-8 text.');
  const pattern=options.pattern??'',flags=options.flags??'g';
  if(typeof pattern!=='string'||pattern.length>4096)throw new Error('Pattern must be a string of at most 4096 characters.');
  if(typeof flags!=='string'||/[^dgimsuy]/.test(flags)||new Set(flags).size!==flags.length)throw new Error('Use each JavaScript flag d, g, i, m, s, u or y at most once.');
  let regex;try{regex=new RegExp(pattern,flags);}catch(error){throw new Error('Invalid regular expression: '+error.message);}
  const limit=options.max_matches===undefined?1000:Number(options.max_matches);
  if(!Number.isInteger(limit)||limit<1||limit>1000)throw new Error('Match limit must be an integer from 1 to 1000.');
  const replace=options.enable_replacement===true||options.enable_replacement==='true',replacement=options.replacement??'';
  if(typeof replacement!=='string'||replacement.length>4096)throw new Error('Replacement must contain at most 4096 characters.');
  const matches=[],raw=[];let truncated=false,budget=0;
  for(;;){
    const match=regex.exec(input);if(!match)break;
    const result={text:match[0],index:match.index,end:match.index+match[0].length,groups:match.slice(1).map(value=>value??null),namedGroups:match.groups?Object.fromEntries(Object.entries(match.groups).map(([key,value])=>[key,value??null])):{}};
    if(match.indices)result.indices={groups:match.indices.map(pair=>pair??null),namedGroups:match.indices.groups?Object.fromEntries(Object.entries(match.indices.groups).map(([key,value])=>[key,value??null])):{}};
    budget+=JSON.stringify(result).length;
    if(matches.length===limit||budget>MAX_OUTPUT){truncated=true;break;}
    matches.push(result);raw.push(match);
    if(!regex.global)break;
    if(match[0]===''){const position=regex.lastIndex;regex.lastIndex=position+(regex.unicode&&input.codePointAt(position)>0xffff?2:1);}
  }
  const report={engine:'JavaScript (ECMAScript)',pattern,flags,indexUnit:'UTF-16 code units',matchCount:matches.length,truncated,matches};
  if(replace){
    if(truncated)report.replacementError='Replacement is unavailable because the match or output limit was reached. Increase the match limit or use a smaller input.';
    else{
      const parts=[];let cursor=0,size=0;
      for(const match of raw){const prefix=input.slice(cursor,match.index),value=substitute(replacement,match,input);size+=prefix.length+value.length;if(size>MAX_OUTPUT)throw new Error('Replacement exceeds the 1 MiB output limit.');parts.push(prefix,value);cursor=match.index+match[0].length;}
      parts.push(input.slice(cursor));const output=parts.join('');if(new TextEncoder().encode(output).length>MAX_OUTPUT)throw new Error('Replacement exceeds the 1 MiB output limit.');report.replacedText=output;
    }
  }
  return report;
}
