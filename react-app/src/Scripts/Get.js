export async function get(ip, community, oid) {
  let get = await getValue(ip, community, oid)
  let value = get.response.value
  return value
}

function getValue(ip, community, oid){
  return fetch(`http://127.0.0.1:8080/get_request?ip_address=${ip}&community=${community}&oid=${oid}`)
  .then((response) => response.json())
}
