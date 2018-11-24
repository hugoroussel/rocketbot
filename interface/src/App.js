import React, { Component } from 'react'
import fetch from 'unfetch'

class App extends Component {
  constructor () {
    super()
    this.state = { teams: [] }
  }

  async componentDidMount () {
    const res = await fetch('http://lauzhack.sqpub.ch/teams')
    const teams = await res.json()
    this.setState({ teams })
  }

  render () {
    const teams = this.state.teams.sort((t1, t2) => t1.cash + t1.assets < t2.cash + t2.assets)
    return (
      <div>
        <h1>Rocket Interface</h1>
        <p>The best trading bot in the universe</p>
        <table>
          <tbody>
            {teams.map(team =>
              <tr
                key={team.id}
                style={team.name === 'Rocket' ? { background: '#c5e7e2' } : {}}
              >
                <td>{team.name}</td>
                <td>{team.cash + team.assets}</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    )
  }
}

export default App
