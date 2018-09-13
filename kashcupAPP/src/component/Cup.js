import React from 'react';
import ImageStateComponent from './ImageStateComponent';

const Cup = (props) => {
  return(
    <div className={"cup"}>
      <ImageStateComponent className={"cupImage"} points={props.points} />
      <p className={"cupPoints"}>{props.points}</p>
      <p className={"cupID"}>#{props.id}</p>
    </div>
  );
}

export default Cup;
