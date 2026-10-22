// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// Source processing rules. Engine loading and process isolation belong to callers.
export const parsers={javascript:'babel',typescript:'typescript',jsx:'babel',tsx:'typescript',html:'html',css:'css',scss:'scss',less:'less',json5:'json5',jsonc:'json',yaml:'yaml',markdown:'markdown',mdx:'mdx',graphql:'graphql',vue:'vue',svelte:'svelte',astro:'astro',solidity:'antlr',php:'php'};
export const pluginPackages={svelte:'prettier-plugin-svelte',astro:'prettier-plugin-astro',solidity:'prettier-plugin-solidity',php:'@prettier/plugin-php'};
export const minifierLanguages=new Set(['javascript','typescript','jsx','tsx','css','html','svg','graphql']);

export async function transformSource({operation,language,text},{load,plugins=async()=>[]}){
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
    const parser=parsers[language];
    if(!parser)throw new Error('No source parser is registered for this language.');
    result=await (await load('prettier')).format(text,{parser,plugins:await plugins(language),...(language==='php'?{phpVersion:'8.5'}:{})});
  }
  if(typeof result!=='string')throw new Error('No source engine is registered for this operation.');
  return result;
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
