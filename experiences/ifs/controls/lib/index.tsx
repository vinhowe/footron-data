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
    display: flex;
    gap: 10px;
    align-items: center;
  }
`;

const ControlsComponent = (): JSX.Element => {
  const [aVal, setAVal] = useState<number>(0);
  const [bVal, setBVal] = useState<number>(0);
  const [cVal, setCVal] = useState<number>(0);
  const [dVal, setDVal] = useState<number>(0);

  const { sendMessage } = useMessaging<any>((message) => {
    const vals = JSON.parse(message);
    setAVal(vals[0]);
    setBVal(vals[1]);
    setCVal(vals[2]);
    setDVal(vals[3]);
  });

  const updateServer = async (vals: unknown) => {
    await sendMessage(vals);
  };

  const serverResume = async (value: unknown) => {
    await sendMessage([value]);
  };

  const handleClick = async (vals: unknown) => {
    updateServer(vals);
  };

  const updateA = async (event: unknown, value: unknown) => {
    setAVal(value);
    updateServer([value, bVal, cVal, dVal]);
  };
  const updateB = async (event: unknown, value: unknown) => {
    setBVal(value);
    updateServer([aVal, value, cVal, dVal]);
  };
  const updateC = async (event: unknown, value: unknown) => {
    setCVal(value);
    updateServer([aVal, bVal, value, dVal]);
  };
  const updateD = async (event: unknown, value: unknown) => {
    setDVal(value);
    updateServer([aVal, bVal, cVal, value]);
  };

  return (
    <div css={containerStyle}>
      <p>
        <b>
          The DeJong iterated functional system is controlled by four values.
          Try your own!
        </b>
      </p>

      <div>
        <div className="slider">
          A:
          <Slider
            min={-3}
            max={3}
            onChange={updateA}
            step={0.0001}
            value={aVal}
          />{" "}
        </div>
        <div className="slider">
          B:{" "}
          <Slider
            min={-3}
            max={3}
            onChange={updateB}
            step={0.0001}
            value={bVal}
          />{" "}
        </div>
        <div className="slider">
          C:{" "}
          <Slider
            min={-3}
            max={3}
            onChange={updateC}
            step={0.0001}
            value={cVal}
          />{" "}
        </div>
        <div className="slider">
          D:{" "}
          <Slider
            min={-3}
            max={3}
            onChange={updateD}
            step={0.0001}
            value={dVal}
          />{" "}
        </div>
      </div>

      <p style={{ marginTop: "15px" }}>
        <b>Or try a predefined setting:</b>
      </p>

      <Box display="flex" flexWrap="wrap" justifyContent="center" p={0} m={0}>
        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([0.8732, -2, 1.6243, 2]);
            }}
          >
            Setting 1
          </Button>
        </Box>

        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([-1.2259, 2.0784, -2.221, 1.3115]);
            }}
          >
            Setting 2
          </Button>
        </Box>

        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([1.5361, 2.0011, 2.5525, 2.6402]);
            }}
          >
            Setting 3
          </Button>
        </Box>

        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([-2, -2, 1, 2]);
            }}
          >
            Setting 4
          </Button>
        </Box>

        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([0.2656, -2.5573, -3, -1.069]);
            }}
          >
            Setting 5
          </Button>
        </Box>

        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              handleClick([-0.5, 0.7, -1.5, -1]);
            }}
          >
            Setting 6
          </Button>
        </Box>
      </Box>

      <Box display="flex" flexWrap="wrap" justifyContent="center" p={0} m={0}>
        <Box p={1} m={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              serverResume(0);
            }}
          >
            Resume
          </Button>
        </Box>
      </Box>
    </div>
  );
};

export default ControlsComponent;
