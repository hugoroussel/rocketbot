import React, { Component } from 'react';

class App extends Component {
  constructor() {
    super()
    this.state = { message: '' }
  }
  render() {
    return (
      <div>
        <h1>Rocket Interface</h1>
        <p>The best trading bot in the universe</p>
      </div>
    );
  }
}

export default App;
