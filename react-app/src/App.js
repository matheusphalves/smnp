import './App.css';
import ClayButton from '@clayui/button';
import ClayCard from '@clayui/card';
import ClayForm, { ClayInput } from '@clayui/form';
import React, { useState } from 'react';

function App() {
  const [hosts, setHosts] = useState([])

  function insertHost(e) {
    e.preventDefault();

    setHosts([...hosts, {
      ip: document.getElementById("ip").value,
      hostName: "LocalHost", //substituir por um get que pega o oid no pc
      response: ""
    }])
  }

  function post(e) {
    e.preventDefault();
    
    fetch("http://127.0.0.1:8080/get_request?ip_address=127.0.0.1&community=public&oid=1.3.6.1.2.1.1.5.0")
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      console.log(data.response.value)
      console.log(data.response.value)
    })
    .catch((error) => console.log( error.response.request._response ) );
  }


  return (
    <>
      <h1>SNMP</h1>
      <ClayForm onSubmit={post}>
        <ClayForm.Group>
          <ClayInput
            id="ip"
            placeholder="Ip"
            type="text"
          />
        </ClayForm.Group>
        <ClayButton className="mt-3 mb-4" type='submit' displayType="primary">
          Add
        </ClayButton>
      </ClayForm>
      {
        hosts.map((host, index) => (
          <ClayCard key={index}>
            <ClayCard.Body>
              <ClayCard.Description displayType="title">
                <strong>{host.hostName}</strong>
              </ClayCard.Description>
              {host.ip}
              <ClayInput
                className="mt-4"
                id="basicInputText"
                placeholder="Insert your OID"
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
