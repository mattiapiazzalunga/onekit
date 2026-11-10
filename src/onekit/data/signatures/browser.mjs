// Copyright 2026 Mattia Piazzalunga
// SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
// The Python adapter consumes the same report envelope in every browser host.
function base64(bytes){
  let value='';
  for(let offset=0;offset<bytes.length;offset+=8192)
    value+=String.fromCharCode(...bytes.subarray(offset,offset+8192));
  return btoa(value);
}

export function browserRuntime(engine){
  return async request=>{
    const input=request.toJs({dict_converter:Object.fromEntries,create_pyproxies:false});
    try{
      const reports=await engine.validate(input);
      return JSON.stringify({schema:'onekit-dss-reports-v1',reports:
        Object.fromEntries(Object.entries(reports).map(([name,data])=>[name,base64(data)]))});
    }catch(error){
      if(!['validation_failed','validation_timeout','engine_failed'].includes(error.message))throw error;
      return JSON.stringify({schema:'onekit-dss-reports-v1',error:'dss_validation_failed'});
    }
  };
}
