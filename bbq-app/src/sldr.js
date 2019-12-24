import React, { Component } from 'react';
//import './App.css';
//import './remote.css';


class Sldr extends Component {
  constructor(props) {
    super(props);
      this.state = {
	  value: 180
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleMouseUp = this.handleMouseUp.bind(this);
    this.handleTouchEnd = this.handleTouchEnd.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  // handle a mouse up event on the slider
  handleMouseUp(event) {
    console.log('Change Color'+event.target.value);
    var localColor = this.state.value;
    console.log("Send Message, color: "+localColor);

    //replace with a general mechanism to send a message
      // 'https://0xdf8rfldc.execute-api.us-east-1.amazonaws.com/prod/setpoint'
      fetch('https://5tvo1710vk.execute-api.us-east-1.amazonaws.com/prod/bbqshadow/desired/set_point?value='+this.state.value, {
      method: 'POST',
      body: JSON.stringify({
        newSetPoint: this.state.value,
        secondParam: 'yourOtherValue',
      })
    })      
  }

  handleTouchEnd(event) {
    console.log('Touch End Change Color'+event.target.value);
    var localColor = this.state.value;
    console.log("Send Message, color: "+localColor);
    // replace with a general mechanism to send a message
      
  }
  

 componentDidMount() {
   console.log('I was triggered during component mount');

   // removed client connect code
 }

  render() {  
    return (
	    <div>
        <p>Set Point </p>
        <p className="slide_text"> {this.state.value} </p>
	<input
	  id="typeinp"
	  type="range"
	  min="0" max="359"
	  value={this.state.value}
	  onChange={this.handleChange}
	  onMouseUp={this.handleMouseUp}
	  onTouchEnd={this.handleTouchEnd}
	step="1"/>
	</div>
    );
  }
}

export default Sldr;
