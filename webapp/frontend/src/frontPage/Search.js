import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));
export default function Search(props) {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      Waddup Boi
      <Grid container spacing={5}>
        <Grid item xs={9}>
            <OutlinedInput id="component-outlined" fullWidth={true} placeholder={"enter sum"}/>
        </Grid>
        <Grid item xs={3}>
          <FormControl variant="outlined" fullWidth={true}>
            <Select
              labelId="demo-simple-select-filled-label"
              id="demo-simple-select-filled"
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              <MenuItem value={10}>Tone-Separation</MenuItem>
              <MenuItem value={20}>Noise-Voice-Separation</MenuItem>
              <MenuItem value={30}>Multi-Speaker-Separation</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>
    </div>
  );
}

