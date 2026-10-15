// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: Apache-2.0
export function packageInstaller(py,dependencies){
  const installed=new Set();
  async function install(name){
    if(installed.has(name))return;
    for(const dependency of dependencies.requires[name]||[])await install(dependency);
    if(dependencies.builtins[name])await py.loadPackage(dependencies.builtins[name]);
    else if(dependencies.packages[name]){
      py.globals.set('_onekit_package',`${name}==${dependencies.packages[name]}`);
      await py.runPythonAsync('import micropip; await micropip.install(_onekit_package, deps=False)');
      py.globals.delete('_onekit_package');
    }else throw new Error(`Browser dependency is not approved: ${name}`);
    installed.add(name);
  }
  return async names=>{for(const name of names)await install(name);};
}
