import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import 'semantic-ui-css/semantic.min.css';
import { Container, Loader, Grid, Card, Popup, Image, Icon, Button, Segment } from 'semantic-ui-react';
import Carousel from 'nuka-carousel';
import headerImage from './header.png';
import axios from 'axios';

import imageState1 from './state_1.png';
import imageState2 from './state_2.png';
import imageState3 from './state_3.png';
import imageState4 from './state_4.png';
import imageState5 from './state_5.png';
import imageState6 from './state_6.png';


const ITEMS_PER_PAGE = 96;

const ImageStateComponent = (props) => {   
  const { total } = props;
  if(total == 0){
    return <Image src={imageState1} />
  }
  else if(total == 1){
    return <Image src={imageState2} />
  }
  else if(total == 2){
    return <Image src={imageState3} />
  }
  else if(total == 3){
    return <Image src={imageState4} />
  }
  else if(total == 4){
    return <Image src={imageState5} />
  }
  else if(total >= 5){
    return <Image src={imageState6} />
  }
}
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: undefined
    }
  }
  // goFirstSlide = () => {
  //   debugger;
  //   this.refs.carousel.goToSlide(null, 3);
  // }
  componentWillMount() {
    axios.get('http://localhost:3000/cupsinfo')
      .then(function (response) {
        debugger;
        var newItems = response.data.map((item) => {
          return {
            id: item.id,
            total: item.total
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

  render() {
    return (
      <div>
        <Image src={headerImage} />
        <Carousel ref="carousel" autoplay={true} vertical={false} speed={1000} autoplayInterval={5000}>
          <div className="slide">
            <Grid>
              {this.state.items && this.state.items.map((item, index) => {
                if (index < ITEMS_PER_PAGE) {
                  return <Grid.Column key={index}>
                    <ImageStateComponent total={item.total} />
                    <p>{item.id}</p>
                  </Grid.Column>
                }
              })}
            </Grid>
          </div>

          <div className="slide">
            <Grid>
              {this.state.items && this.state.items.map((item, index) => {
                if (index >= ITEMS_PER_PAGE && index < ITEMS_PER_PAGE * 2) {
                  return <Grid.Column key={index}>
                  <ImageStateComponent total={item.total} />
                    <p>{item.id}</p>
                  </Grid.Column>
                }
              })}
            </Grid>
          </div>

          <div className="slide">
            <Grid>
              {this.state.items && this.state.items.map((item, index) => {
                if (index >= ITEMS_PER_PAGE * 2 && index < ITEMS_PER_PAGE * 4) {
                  return <Grid.Column key={index}>
                  <ImageStateComponent total={item.total} />
                    <p>{item.id}</p>
                  </Grid.Column>
                }
              })}
            </Grid>
          </div>

        </Carousel>
      </div>
    );
  }
}

export default App;
