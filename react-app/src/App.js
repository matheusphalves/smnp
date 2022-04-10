import './App.css';
import ClayButton from '@clayui/button';
import ClayCard from '@clayui/card';
import ClayForm, { ClayInput } from '@clayui/form';
import React, { useState } from 'react';
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
              <ClayCard.Description displayType="title">
                <strong>Hostname: </strong>
                {host.hostName}
              </ClayCard.Description>
              <strong>IP: </strong>
              {host.ip}
              <br></br>
              <strong>Community: </strong>
              {host.community}
              <ClayInput
                className="mt-4"
                id="basicInputText"
                placeholder="Insert OID"
                type="text"
              />
              <ClayButton className="mt-2">{"Get"}</ClayButton>
              <ClayCard.Description className="mt-4" truncate={false} displayType="text">
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
