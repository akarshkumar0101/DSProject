import React, { useState, useEffect ,Component} from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import Blog from './frontPage/Blog'
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Header from './frontPage/Header';
import Search from './frontPage/Search';
import FeaturedPost from './frontPage/FeaturedPost';
import Main from './frontPage/Main';
import Sidebar from './frontPage/Sidebar';
import Footer from './frontPage/Footer';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormLabel from '@material-ui/core/FormLabel';
import Button from '@material-ui/core/Button';
import FormHelperText from '@material-ui/core/FormHelperText';





// const useStyles = makeStyles((theme) => ({
//   mainGrid: {
//     marginTop: theme.spacing(3),
//   },
// }));
// const classes = useStyles();


const sections = [
  { title: 'Home', url: '#' },
  { title: 'About Us', url: '#' },
  { title: 'Blog', url: '#' }
];

const sidebar = {
  title: 'Random',
  description:
    'Etiam porta sem malesuada magna mollis euismod. Cras mattis consectetur purus sit amet fermentum. Aenean lacinia bibendum nulla sed consectetur.',
  archives: [
  ],
  social: [
  ],
};

// const [value, setValue] = React.useState('female');

//   const handleChange = (event) => {
//     setValue(event.target.value);
// };


class FrontPage extends Component{

    constructor(props){
        super(props)
        this.state = {
            originalURL:"",
            model:"",
            mix:"None",
            modelErrorMessage:"",
            modelError:false,
            originalURLError:false,
            originalURLErrorMessage:"",
            modelResult:"",
            modelResult:""
        }
        this.handleChangeOriginalURL = this.handleChangeOriginalURL.bind(this);
        this.handleChangeMethod = this.handleChangeMethod.bind(this);
        this.handleChangeMix = this.handleChangeMix.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.getResults = this.getResults.bind(this);
    }

    getResults(){
        var scope = this
        axios.get("https://speech-separation-api.herokuapp.com")
        .then(function (respo) {
            // console.log(respo)
            scope.setState({
                 modelResult:respo.data
            }); 
        })
    }

    handleChangeOriginalURL(event){
        let newVal = (event.target.value ? event.target.value : "");
        this.setState(state =>(
            {originalURL: newVal }
        ))
    }
    handleChangeMethod(event){
        console.log(event.target.value)
        let newVal = (event.target.value ? event.target.value : "");
        this.setState(state =>(
            {model: newVal}
        ))
    }
    handleChangeMix(event){
        console.log(event.target.value)
        let newVal = (event.target.value ? event.target.value : "None")
        this.setState(state =>(
            {mix: newVal}
        ))
    }
    handleClick(){
        //check for errors
        if(this.state.model==""){
            this.setState(state =>(
                {modelError:true,
                modelErrorMessage:"Error: Choose what you want to separate"}
            ))
        }else{
            this.setState(state =>(
                {modelError:false,
                modelErrorMessage:""}
            ))
        } if(this.state.originalURL==""){
            this.setState(state =>(
                {
                    originalURLError:true,
                    originalURLErrorMessage: "Error"
                }
            ))
        } else{
            this.setState(state =>(
                {
                    originalURLError:false,
                    originalURLErrorMessage: ""
                }
            ))
        }
        if(this.state.model=="" || this.state.originalURL=="")
            return;
        //all errors have been checked for
        //do a get request to the backend to do a feed forward
        this.getResults()
    }

render(){

  return (

    <React.Fragment>
      <CssBaseline />
      <Container maxWidth="lg">
        <Header title="Sound Surgeon" sections={sections} />
        <main>
          <Grid container spacing={12}>
            <h3> Step 1: Enter URL of Origninal Audio Source</h3>
            <Grid item xs={9}>
            <FormControl error={this.state.originalURLError} fullWidth={true}>
              <OutlinedInput 
                id="component-outlined" fullWidth={true} placeholder={"Enter URL to your original audio audio file..."}
                value = {this.state.originalURL} onChange={this.handleChangeOriginalURL}             
              />
            <FormHelperText id="component-error-text">{this.originalURLErrorMessage}</FormHelperText>
            </FormControl>
            </Grid>
          </Grid>
          
          <Grid container spacing={12}>
            
          <h3> Step 2: Select What You Want Separated From Your Audio</h3>
            <Grid item xs={9}>
            <FormControl component="fieldset" error={this.state.modelError}>
            <RadioGroup aria-label="gender" name="gender1" value={this.state.model} onChange={this.handleChangeMethod}>
              <FormControlLabel value="Tone" control={<Radio />} label="Note/Tone"/>
              <FormControlLabel value="Noise" control={<Radio />} label="Noise/Air Conditioning" />
              <FormControlLabel value="MultiSpeaker" control={<Radio />} label="Multiple Speakers" />
              <FormControlLabel value="Dog" control={<Radio />} label="Dog Barking" />
              <FormHelperText>{this.state.modelErrorMessage}</FormHelperText>
            </RadioGroup>
            </FormControl>
            </Grid>
          </Grid>
          
          <Grid container spacing={12}>
            
          <h3> Step 3: (Not Required if Your Input is Already Mixed) Add a Sound to Your Original Audio File to Test our Model</h3>
            <Grid item xs={9}>
            <FormControl component="fieldset">
            <RadioGroup defaultValue="None" aria-label="gender" name="gender1" value={this.state.mix} onChange={this.handleChangeMix}>
              <FormControlLabel value="Tone" control={<Radio />} label="Note/Tone of random Frequency between 1000 and 3700"/>
              <FormControlLabel value="Noise" control={<Radio />} label="Random Noise/Air Conditioning Noise from LibriSpeech Dataset" />
              <FormControlLabel value="MultiSpeaker" control={<Radio />} label="Multiple Speakers" />
              <FormControlLabel value="Dog" control={<Radio />} label="Random Dog Barking Noise from UrbanSounds Dataset" />
              <FormControlLabel value="None" control={<Radio />} label="None" />

            </RadioGroup>
            </FormControl>
            </Grid>
          </Grid>

          <Grid container spacing={12}>
            <h3> Step 4: Run the Model</h3>
            <Grid item xs={12}>
              <Button variant="contained" onClick = {this.handleClick}>Run</Button>
            </Grid>
          </Grid>         
        
          <Grid container spacing={5}>
            <Main title={this.state.modelResult} posts={[]} />
            <Sidebar
              title={sidebar.title}
              description={sidebar.description}
              archives={sidebar.archives}
              social={sidebar.social}
            />
          </Grid>

           

        </main>
      </Container>
      <Footer title="Footer" description="Something here to give the footer a purpose!" />
    </React.Fragment>
  );
  }
}

export default FrontPage;
