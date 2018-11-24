import React, { Component } from 'react'
import fetch from 'unfetch'

class App extends Component {
  constructor () {
    super()
    this.state = {
      teams: [],
      transactions: [],
      interval: 0
    }
    this.getValues = this.getValues.bind(this)
  }

  async componentDidMount () {
    await this.getValues()
    const interval = setInterval(this.getValues, 2000)
    this.setState({ interval })
  }
  
  componentWillUnmount () {
    clearInterval(this.state.interval)
  }
  
  async getValues () {
    const getTeams = await fetch('http://lauzhack.sqpub.ch/teams')
    const getTransactions = await fetch('http://localhost:5000/transactions')
    const teams = await getTeams.json()
    const transactions = await getTransactions.json()
    this.setState({ teams, transactions })
  }

  render () {
    const teams = this.state.teams.sort((t1, t2) => t1.cash + t1.assets < t2.cash + t2.assets)
    return (
      <div>
        <h1 style={{ textAlign: 'center' }}>Rocket Bot Interface</h1>
        <div style={{ display: 'flex' }}>
          <div style={{ flexGrow: 2 }}>
            <h2 style={{ textAlign: 'center' }}>Current Ranking</h2>
            <table style={{ width: '100%' }}>
              <tbody>
                {teams.map(team =>
                  <tr
                    key={team.id}
                    style={team.name === 'Rocket' ? { background: '#c5e7e2' } : {}}
                  >
                    <td>{team.name}</td>
                    <td>{team.cash + team.assets}</td>
                    <td>{team.XBT}</td>
                    <td><progress max={team.cash + team.assets} value={team.assets}></progress></td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <div style={{ flexGrow: 1 }}>
            <h2 style={{ textAlign: 'center' }}>Latest Transactions</h2>
            <ul>
              {this.state.transactions.map(tx => {
                if (tx.received_at) {
                  return (
                    <li key={tx.received_at}>
                      <pre>
                        {tx.received_at} ~ {tx.order_type} {tx.quantity} {tx.currency}
                      </pre>
                    </li>
                  )
                } else {
                  return (
                    <li>{ tx }</li>
                  )
                }
              }
              )}
            </ul>
          </div>
        </div>
      </div>
    )
  }
}

export default App
