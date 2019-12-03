import React, {Component, PureComponent} from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

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
        <XAxis dataKey="qtime" />
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
    render() {
	let {temps, isLoading} = this.state;
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
		    <h1> Set Point: {temps.Items[0].setPoint} </h1>
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
        temps: []
	
    };

    componentDidMount() {
	console.log("component mounted");
	//fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl')
	fetch('https://yb2g5joqs7.execute-api.us-east-1.amazonaws.com/prod/bbqctrl2')

            .then(res => res.json())
            .then((data) => {
                this.setState({ temps: data,
				isLoading: false});
		
            })
            .catch(console.log)
	console.log("done fetch1");
	console.log("done fetch2");
	
    }
}

export default App;

