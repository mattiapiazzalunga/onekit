// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import initialize,{main} from './tex_fmt.mjs';
let ready;
export function init({url=new URL('./tex_fmt_bg.wasm',import.meta.url),bytes}={}) {
  return ready??=initialize({module_or_path:bytes||url}).catch(error=>{ready=undefined;throw error;});
}
export function format(text) {
  if(typeof text!=='string'||new TextEncoder().encode(text).length>256*1024)throw new Error('Source is too complex. Split it into smaller files.');
  const result=main(text,'wrap = true\nwraplen = 80\ntabsize = 2\nusetabs = false\n');
  if(typeof result.output!=='string'||new TextEncoder().encode(result.output).length>4*1024*1024)throw new Error('No source engine is registered for this operation.');
  return result.output;
}
