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

const ControlsComponent = () => {
    const [majorIndVal, setMajorIndVal] = useState(0);
    const [minorIndVal, setMinorIndVal] = useState(0);

    const { sendMessage } = useMessaging((message) => {
        setMajorIndVal( message[0] );
        setMinorIndVal( message[1] );
    });

    const handleClick = async ( val ) => {
        await sendMessage( ['img',val] );
    };

    const handleResume = async () => {
        await sendMessage( ['resume'] );
    };

    const handleMajorSlider = async ( event, val ) => {
        setMajorIndVal( val );
        await sendMessage( ['inds',val,minorIndVal] );
    };

    const handleMinorSlider = async ( event, val ) => {
        setMinorIndVal( val );
        await sendMessage( ['inds',majorIndVal,val] );
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
            <b>Try scrubbing the sliders to watch the pixels on their epic journey.  The top one advances the pixels exactly 1024 steps; the bottom one advances the pixels exactly one step:</b>
        </p>

            <Slider min={0} max={1024} onChange={handleMajorSlider} value={majorIndVal} />
            <Slider min={0} max={1023} onChange={handleMinorSlider} value={minorIndVal} />

      </Box>

      <Box
        display="flex"
        flexWrap="wrap"
        justifyContent="center"
        p={0}
        m={0}
      >
        <p>
            <b>Or try changing to different images to better understand the pattern:</b>
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
            <Button variant="contained" color="primary" onClick={() => { handleClick(1) }}>
            BYU Logo
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(2) }}>
            Black and White
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(3) }}>
            Jerod Lessar
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(4) }}>
            Rainbow
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(5) }}>
            Abby Stainton
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(6) }}>
            Butterfly
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(7) }}>
            Dancers
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(8) }}>
            Marriott Center
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(9) }}>
            The moon
            </Button>
            </Box>

            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleClick(10) }}>
            Studying
            </Button>
            </Box>

        </Box>

      <Box
        display="flex"
        flexWrap="wrap"
        justifyContent="center"
        p={0}
        m={0}
      >
            <Box p={0.5} m={1}>
            <Button variant="contained" color="primary" onClick={() => { handleResume() }}>
            Resume animation
            </Button>
            </Box>

        </Box>

    </div>
  );
};

export default ControlsComponent;
