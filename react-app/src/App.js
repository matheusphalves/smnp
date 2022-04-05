import './App.css';
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { useState } from 'react';

function App() {
  const [informations, setInformations] = useState()

  return (
    <div className="App">
      <header className="App-header">
        <h1>SNMP</h1>
        <Form>
          <div key={`inline-radio`} className="mb-3">
            <Form.Check
              inline
              label="Temperatura"
              name="group1"
              type="radio"
              id={`inline-radio-1`}
            />
            <Form.Check
              inline
              label="HostName"
              name="group1"
              type="radio"
              id={`inline-radio-2`}
            />
            <Form.Check
              inline
              label="Other Information"
              name="group1"
              type="radio"
              id={`inline-radio-3`}
            />
          </div>
        </Form>
        <Button variant="primary" onClick={() => setInformations("informações vindas do agente!!!")}>Buscar Informação</Button>

        {
          informations
        }
      </header>
    </div>
  );
}

export default App;
