import React from 'react';

import imageState1 from '../img/state_1.png';
import imageState2 from '../img/state_2.png';
import imageState3 from '../img/state_3.png';
import imageState4 from '../img/state_4.png';
import imageState5 from '../img/state_5.png';
import imageState6 from '../img/state_6.png';

const ImageStateComponent = (props) => {
  const { points } = props;
  switch (true) {
    case (points<=10):
      return <img className={"cupIMG"} src={imageState2} />
    case (points>10 && points<=25):
      return <img className={"cupIMG"} src={imageState3} />
    case (points>25 && points<=50):
      return <img className={"cupIMG"} src={imageState4} />
    case (points>50 && points<=75):
      return <img className={"cupIMG"} src={imageState5} />
    case (points>=100):
      return <img className={"cupIMG"} src={imageState6} />
    default:
      return <img className={"cupIMG"}src={imageState1} />
  }
};

export default ImageStateComponent;
