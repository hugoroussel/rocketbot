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
    const teams = await getTeams.json()
    this.setState({ teams })
    const getTransactions = await fetch('http://localhost:5000/transactions')
    const transactions = JSON.parse(await getTransactions.json())
    this.setState({ transactions })
  }

  render () {
    const teams = this.state.teams
      .map(t => ({ cash: parseInt(t.cash), assets: parseInt(t.assets), ...t }))
      .sort((t1, t2) => t1.cash + t1.assets < t2.cash + t2.assets)
    const transactions = this.state.transactions.slice().reverse().slice(0, 10)
    return (
      <div>
        <h1 style={{ textAlign: 'center' }}><span role='img' aria-label='rocket'>🚀</span> Bot Interface</h1>
        <div style={{ display: 'flex' }}>
          <div style={{ flexGrow: 2 }}>
            <h2 style={{ textAlign: 'center' }}>Current Ranking</h2>
            <table style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th>Team Name</th>
                  <th>Total (USD)</th>
                  <th>XBTs</th>
                  <th>XBT Ratio</th>
                </tr>
              </thead>
              <tbody>
                {teams.map(team =>
                  <tr
                    key={team.id}
                    style={team.name === 'Rocket' ? { background: '#c5e7e2' } : {}}
                  >
                    <td>{team.name}</td>
                    <td>{team.cash + team.assets}</td>
                    <td>{team.XBT}</td>
                    <td><progress max={team.cash + team.assets} value={team.assets} style={{ width: '100%' }} /></td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <div style={{ flexGrow: 1 }}>
            <h2 style={{ textAlign: 'center' }}>Latest Transactions</h2>
            <ul>
              {transactions.map(tx => {
                tx = JSON.parse(tx[0].replace(/'/gi, '"'))
                if (tx.received_at) {
                  return (
                    <li key={tx.received_at}>
                      <pre>
                        {tx.received_at} ~ {tx.order_type} {tx.quantity} {tx.currency} @ {tx.unit_price}
                      </pre>
                    </li>
                  )
                } else {
                  return (
                    <li key={tx}><pre>{ tx }</pre></li>
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
