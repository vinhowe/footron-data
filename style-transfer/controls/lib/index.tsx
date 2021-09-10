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
    const { sendMessage } = useMessaging<any>((message) => {
console.log( "Got message:", message );
    });

    const handleClick = async ( val ) => {
await sendMessage(val);
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
          <b>Try changing to different styles!</b>
        </p>
      </Box>

      <Box
        display="flex"
        flexWrap="wrap"
        justifyContent="center"
        p={0}
        m={0}
      >
            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("feathers.jpg") }}>
            Feathers
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("pencil.jpg") }}>
            Pencil Sketch
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("la_muse.jpg") }}>
            Pablo Picasso - La Muse
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("frida_kahlo.jpg") }}>
            Frido Kahlo - Self-Portrait
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("udnie.jpg") }}>
            Francis Picabia - Udnie
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("roman_ducks.jpg") }}>
            3rd Century Roman Mosaic
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("glass_mosaic.jpg") }}>
            Mosaic on glass
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick("pollack.jpg") }}>
            Jackson Pollack - Picture Peddler #14
            </Button>
            </Box>

      </Box>

    </div>
  );
};

export default ControlsComponent;
