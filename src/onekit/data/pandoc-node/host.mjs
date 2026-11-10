// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: GPL-2.0-or-later
// Standalone Pandoc engine host, used across a process/worker message boundary.
export async function convert(instance,request) {
  if(!request||typeof request.stdin!=='string'||new TextEncoder().encode(request.stdin).length>256*1024)throw Error('Document conversion failed.');
  const o=request.options;
  if(!o||Object.keys(o).sort().join(',')!=='from,sandbox,to'||o.from!=='latex'||!['html','markdown'].includes(o.to)||o.sandbox!==true)throw Error('Document conversion failed.');
  const result=await instance.convert(o,request.stdin,{});
  if(typeof result.stdout!=='string'||new TextEncoder().encode(result.stdout).length>4*1024*1024||result.stderr||result.warnings?.length)throw Error('Document conversion failed.');
  return {stdout:result.stdout,stderr:'',warnings:[]};
}
