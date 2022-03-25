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
    const [numParticles, setNumParticles] = useState<number>(65536);
    const [fade, setFade] = useState<number>(0.996);
    const [speed, setSpeed] = useState<number>(0.25);

    const { sendMessage } = useMessaging<any>((message) => {
        // we're not expecting any messages from the server
        console.log( message );
    });

    const updateServer = async (vals: unknown) => {
        await sendMessage(vals);
    };

    const updateNP = async (event: unknown, value: unknown) => {
        setNumParticles(value);
        updateServer( { numParticles:value, fade:fade, speed:speed } );
    };

    const updateFade = async (event: unknown, value: unknown) => {
        setFade(value);
        updateServer( { numParticles:numParticles, fade:value, speed:speed } );
    };

    const updateC = async (event: unknown, value: unknown) => {
        setSpeed(value);
        updateServer( { numParticles:numParticles, fade:fade, speed:value } );
    };

  return (
    <div css={containerStyle}>
      <p>
        <b>
          This wind visualization has several parameters you can explore:
        </b>
      </p>

      <div>
        <div className="slider">
          Number of particles:
          <Slider
            min={1024}
            max={589824}
            onChange={updateNP}
            step={1}
            value={numParticles}
          />{" "}
        </div>
        <div className="slider">
          Fade:{" "}
          <Slider
            min={0.96}
            max={0.999}
            onChange={updateFade}
            step={0.0001}
            value={fade}
          />{" "}
        </div>
        <div className="slider">
          Speed:{" "}
          <Slider
            min={0.05}
            max={1.0}
            onChange={updateC}
            step={0.01}
            value={speed}
          />{" "}
        </div>
      </div>

    </div>
  );
};

export default ControlsComponent;
