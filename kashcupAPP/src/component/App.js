import React, { Component} from 'react';
import logo from '../img/logo.svg';
import '../style/index.css';
import 'semantic-ui-css/semantic.min.css';
import axios from 'axios';

import headerImage from '../img/header.png';
import Cup from '../component/Cup';
import Export from '../component/Export';

const ITEMS_PER_PAGE = 100;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: undefined,
      toggle: 0
    }
  }

  componentDidMount() {
    this.interval = setInterval(() => {
      this.getCupData();
    }, 5000);
  }

  handleToggle = () => {
    this.setState({toggle: !this.state.toggle});
  }

  getCupData = () => {
    console.log("Data refresh!");
    axios.get('http://localhost:3000/cupsinfo')
      .then(function (response) {
        // console.log(response)
        let newItems = response.data.map((item) => {
          return {
            id: item.id,
            total: item.total,
            points: item.points
          }
        });
        this.setState({
          items: newItems
        });
      }.bind(this))
      .catch(function (error) {
        console.log(error);
      });
  }

  cupList = () => {
    return(
      <ul className={"cupList"}>
        {this.state.items && this.state.items.map((cup, index) => {
          return <li className={"cupContainer"} key={index}>
            <Cup id={cup.id} points={cup.points} />
          </li>
        })}
      </ul>
    );
  }

  render() {
    return (
      <div className={"container"}>
        <img className={"headerImage"} src={headerImage} onClick={this.handleToggle} />
        <div className={"cupListContainer"}>
          {this.state.toggle ? <Export /> : this.cupList()}
        </div>
      </div>
    )
  }
}

export default App;
