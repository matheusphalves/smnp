import './App.css';
import ClayButton from '@clayui/button';
import ClayCard from '@clayui/card';
import ClayForm, { ClayInput } from '@clayui/form';
import React, { useEffect, useState } from 'react';
import { get } from './Scripts/Get';

function App() {
  const [hosts, setHosts] = useState([])

  async function insertHost(ip, community) {

    let value = await get(ip, community, '1.3.6.1.2.1.1.5.0')

    setHosts([...hosts, {
      ip: ip,
      hostName: value,
      community: community,
      response: null
    }])
  }

  async function getValue(host, oid) {
    let response = await get(host.ip, host.community, oid)

    let newHosts = hosts.map((hostForEach) => {
      if (hostForEach.ip === host.ip) {
        hostForEach["response"] = response
      }

      return hostForEach
    })

    setHosts(newHosts)
  }

  return (
    <>
      <h1>SNMP</h1>
      <ClayForm>
        <ClayInput
          id="ip"
          placeholder="Ip"
          type="text"
        />
        <ClayInput
          id="community"
          placeholder="Community"
          type="text"
        />
        <ClayButton className="mt-3 mb-4"
          onClick={() => insertHost(
            document.getElementById("ip").value,
            document.getElementById("community").value
          )} displayType="primary">
          Add
        </ClayButton>
      </ClayForm>
      {
        hosts.map((host, index) => (
          <ClayCard key={index}>
            <ClayCard.Body>
              <ClayCard.Description displayType="title" value={host.hostName}>
                <strong>Hostname: </strong>
                {host.hostName}
                <span className="material-icons" style={{color: 'green'}}>
                  check_circle
                </span>
                <span className="material-icons" style={{color: 'red'}}>
                  cancel
                </span>
              </ClayCard.Description>
              <strong>IP: </strong>
              {host.ip}
              <br></br>
              <strong>Community: </strong>
              {host.community}
              <ClayInput
                className="mt-4"
                id="oid"
                placeholder="Insert OID"
                type="text"
              />
              <ClayButton className="mt-2"
                onClick={() => getValue(host, document.getElementById("oid").value)}>
                {"Get"}
              </ClayButton>
              <ClayCard.Description className="mt-4" truncate={false} displayType="text">
                <strong>Response: </strong>
                {host.response}
              </ClayCard.Description>
            </ClayCard.Body>
          </ClayCard>
        ))
      }
    </>
  );
}

export default App;
