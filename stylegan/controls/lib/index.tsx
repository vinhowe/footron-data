// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
/** @jsxImportSource @emotion/react */
import { css } from "@emotion/react";
import React, { useCallback, useState, useEffect } from "react";
import { useMessaging } from "@footron/controls-client";
import { Box, Button, Slider } from "@material-ui/core";

const containerStyle = css`
  padding: 16px;
  overflow-x: hidden;

  p {
    margin: 0 0 16px;
  }

  .slider {
    display:flex;
    gap:10px;
    align-items:center;
  }
`;

const ControlsComponent = (): JSX.Element => {
    const [interpVal, setInterpVal] = useState<number>(0);

    const { sendMessage } = useMessaging<any>((message) => {
        console.log( "Got message:", message );
    });

    const handleClick = async ( msg, ival ) => {
        setInterpVal( ival );
        await sendMessage( msg );
    };

    const handleInterpSlider = async ( event, val ) => {
        setInterpVal( val );
        await sendMessage( {'type':'interp_val', 'val':val} );
    };

    return (
            <div css={containerStyle}>
      <Box
        display="flex"
        flexWrap="wrap"
        justifyContent="center"
        p={0}
        m={0}
      >
        <p>
            <b>Create your own face by interpolating between two faces.  Use the buttons below to generate faces, then try interpolating between them with this slider!</b>
        </p>

            <Slider min={0} max={1.0} step={0.001} onChange={handleInterpSlider} value={interpVal} />


            <Box p={1} m={1} justifyContent="center">

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}> <b>Face #1:</b> </Box>

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}>
              <Button variant="contained" color="primary" onClick={() => { handleClick( {'type':'random1'}, 0.0 ) }}>
              Random
            </Button>
            </Box>

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick( {'type':'capture1'}, 0.0 ) }}>
            Capture Current
            </Button>
            </Box>

            </Box>


            <Box p={1} m={1} justifyContent="center">

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}> <b>Face #2:</b> </Box>

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}>
              <Button variant="contained" color="primary" onClick={() => { handleClick( {'type':'random2'}, 1.0 ) }}>
              Random
            </Button>
            </Box>

            <Box display="flex" flexWrap="wrap" justifyContent="center" p={1} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick( {'type':'capture2'}, 1.0 ) }}>
            Capture Current
            </Button>
            </Box>

            </Box>


        </Box>

    </div>
  );
};

export default ControlsComponent;
