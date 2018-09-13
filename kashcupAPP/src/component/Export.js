import React, { Component} from 'react';
import '../style/index.css';
import axios from 'axios';

class Export extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: '',
      userID: 'nan',
      userPoints: 'nan'
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({inputValue: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    axios.post('http://localhost:3000/export', {
      id: this.state.inputValue
    })
    .then((response) => {
      this.setState({
        userID: response.data[0],
        userPoints: response.data[1]
      });
    })
    .catch((error) => {
      console.log(error);
      alert("Please Enter Valid #ID")
    });
  }

  render() {
    return (
      <div className={"container"}>
        <form onSubmit={this.handleSubmit}>
        <label>
          #ID:
          <input type="number" value={this.state.inputValue} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      <div className={"userData"}>
        <p className={"userID"}>User ID: #{this.state.userID}</p>
        <p className={"userPoints"}>User Points: {this.state.userPoints}</p>
      </div>
      </div>
    )
  }
}

export default Export;
