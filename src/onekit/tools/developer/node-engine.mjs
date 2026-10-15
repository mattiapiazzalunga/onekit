// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: Apache-2.0
import {createRequire} from 'node:module';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const require=createRequire(resolve(process.argv[2],'package.json'));
const chunks=[];for await(const chunk of process.stdin)chunks.push(chunk);
const {operation,language,text}=JSON.parse(Buffer.concat(chunks).toString());
try{
  let result;
  if(operation==='minify'){
    if(['javascript','typescript','jsx','tsx','css'].includes(language))result=(await require('esbuild').transform(text,{minify:true,loader:({javascript:'js',typescript:'ts'})[language]||language})).code;
    else if(language==='html')result=await require('html-minifier-terser').minify(text,{collapseWhitespace:true,removeComments:true});
    else if(language==='svg')result=require('svgo').optimize(text).data;
    else if(language==='graphql')result=require('graphql').stripIgnoredCharacters(text);
  }else{
    const parser=({javascript:'babel',typescript:'typescript',jsx:'babel',tsx:'typescript',html:'html',css:'css',scss:'scss',less:'less',json5:'json5',jsonc:'json',yaml:'yaml',markdown:'markdown',mdx:'mdx',graphql:'graphql',vue:'vue',svelte:'svelte',astro:'astro',solidity:'antlr',php:'php'})[language];
    if(!parser)throw new Error('No Node parser is registered for this language.');
    const packageName=({svelte:'prettier-plugin-svelte',astro:'prettier-plugin-astro',solidity:'prettier-plugin-solidity',php:'@prettier/plugin-php'})[language];
    const plugins=[];
    if(packageName)plugins.push((await import(pathToFileURL(require.resolve(packageName)).href)).default||await import(pathToFileURL(require.resolve(packageName)).href));
    result=await require('prettier').format(text,{parser,plugins});
  }
  if(typeof result!=='string')throw new Error('No Node engine is registered for this operation.');
  process.stdout.write(result);
}catch(error){process.stderr.write(String(error.message).slice(0,2000));process.exit(1);}
