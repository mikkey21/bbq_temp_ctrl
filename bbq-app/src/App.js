// git status
// git add <files>
// git commit -m "message"


import React, { Component, PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';
import Sldr from './sldr';

class Example extends PureComponent {
    
  //static jsfiddleUrl = 'https://jsfiddle.net/alidingling/xqjtetw0/';
    
  render() {
      var ctemps = this.props.temps.Items;
      console.log('ctemps',ctemps);	
    return (
	
	<LineChart
        width={500}
        height={300}
        data={ctemps}
        margin={{
          top: 5, right: 30, left: 20, bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
            <Legend />
        <Line type="monotone" dataKey="meatCurrTemp1" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="meatCurrTemp2" stroke="#82ca9d" />
        <Line type="monotone" dataKey="setPoint" stroke="#82ca9d" />
        <Line type="monotone" dataKey="eggCurrTemp1" stroke="#82ca9d" />
      </LineChart>
    );
  }
}




var json_output =
    { Item: 
   { setPoint: 270,
     date: '2019-11-30',
     meatCurrTemp1: 53.9,
     dateTime: '2019-11-30 09:16:41',
     eggAvgTemp: 53.18,
     time: '09:16:36',
     fanState: 'on',
     eggCurrTemp1: 53.18,
     meatCurrTemp2: 55.18 } };

class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    let {temps, isLoading, desiredShadow} = this.state;
    let myItems;
    let tmp1;
    
    if (isLoading) {
      return <div> Loading...</div>;
    } else {
      console.log('temps ',temps);
      myItems = temps.Items;
      console.log('Items ',myItems);
      console.log('Item2 ',temps.Items);
      tmp1 = myItems[1];
      console.log('sample1 ',tmp1);
      return (
          <div>
          <h1> Set Point: {desiredShadow.set_point} </h1>
          <h1> Done Point: {desiredShadow.done_temp} </h1>
          <h1> Fan State: {desiredShadow.status} </h1>
          <form>
            <fieldset>
              Set Point:
          <input type="text" setpoint="setPoint" />
              Done Temp:
      	  <input type="text" donetemp="doneTemp" value={this.state.doneTemp} onChange={(e) => this.handleDoneTempChange(e)} onBlur={(e) => this.handleBlurTempChange(e)} />
            </fieldset>
          </form>
          <Sldr/>
          <Example temps={temps}/>
          <ul>
          {temps.Items.map(item => (
              <li key={item.qtime}>
              Time: {item.qtime} |
              Egg temp: {item.eggAvgTemp} |
              Set Point: {item.setPoint} |
              Q temp: {item.eggAvgTemp} |
              Meat1: {item.meatCurrTemp1} |
              Meat2: {item.meatCurrTemp2}
            </li>
          ))}
	</ul>
          </div>
      )
    }
  }

  state = {
    isLoading: true,
    temps: [],
    desiredShadow: {},
    doneTemp: 120
  };

  handleDoneTempChange(event) {
    console.log("changing done temp: ", this.state.doneTemp);
    console.log('input event', event);
    this.setState({ doneTemp: event.target.value });
  }
  handleBlurTempChange(event) {
    console.log("changing done temp: ", this.state.doneTemp);
    console.log('blur event', event);
    fetch('https://5tvo1710vk.execute-api.us-east-1.amazonaws.com/prod/bbqshadow/desired/done_temp?value=' + event.target.value, {
      method: 'POST',
      body: JSON.stringify({
        newSetPoint: this.state.value,
        secondParam: 'yourOtherValue',
      })
    })
  }

  componentDidMount() {
    console.log("component mounted");
    var apiRequest1 = fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl2').then(function (response) {
      return response.json()
    });
    var apiRequest2 = fetch('https://5tvo1710vk.execute-api.us-east-1.amazonaws.com/prod/bbqshadow/desired').then(function (response) {
      return response.json()
    });
    var combinedData = { "apiRequest1": {}, "apiRequest2": {} };
    //    Promise.all([apiRequest1, apiRequest2]).then(function (values) {
    Promise.all([apiRequest1, apiRequest2]).then((values) => {
      combinedData["apiRequest1"] = values[0];
      combinedData["apiRequest2"] = values[1];
      console.log("combinedData", combinedData);
      console.log("combinedData", combinedData["apiRequest1"]);
      console.log("combinedData", combinedData["apiRequest2"]);
      console.log("this", this);
      this.setState({
        temps: combinedData["apiRequest1"], desiredShadow: combinedData["apiRequest2"], isLoading: false
      }); // this.setState
      this.getData();
    }); // .then
  };

  componentWillUnmount() {
    /*
      stop getData() from continuing to run even
      after unmounting this component. Notice we are calling
      'clearTimeout()` here rather than `clearInterval()` as
      in the previous example.
    */
    clearTimeout(this.intervalID);
  }

  getData = () => {
    console.log("component mounted");
    fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl2')
      .then(res => res.json())
      .then((data) => {
        this.setState({ temps: data, isLoading: false });
        // call getData() again in 5 seconds
        this.intervalID = setTimeout(this.getData.bind(this), 5000);
      })
      .catch(console.log)
  }

  componentDidMount2() {
    console.log("component mounted");
    //fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl')
    fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl2')
      .then(res => res.json())
      .then((data) => {
        this.setState({temps: data, isLoading: false});
      })
    .catch(console.log)
    console.log("fetch the shadow state - desired");
    fetch('https://5tvo1710vk.execute-api.us-east-1.amazonaws.com/prod/bbqshadow/desired')
      .then(res => res.json())
      .then((data) => {
        this.setState({ desiredShadow: data, isLoading: false});
	this.setState({doneTemp: data.done_temp});
	console.log('this',this);
      })
    .catch(console.log)
    console.log("done fetch2");
  }
}

export default App;

