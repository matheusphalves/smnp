export async function get(ip, community, oid) {
  let get = await getValue(ip, community, oid)
  let value = get.response.value
  return value
}

function getValue(ip, community, oid){
  return fetch(`http://127.0.0.1:8080/get_request?ip_address=${ip}&community=${community}&oid=${oid}`)
  .then((response) => response.json())
}

export async function avaliability(ip){
  let status = await checkHealth(ip)
  let value = status.status
  return value
}

function checkHealth(ip){
  return fetch(`http://127.0.0.1:8080/health?ip_address=${ip}`)
  .then((response) => response.json())
}