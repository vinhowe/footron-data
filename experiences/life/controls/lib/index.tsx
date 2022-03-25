/** @jsxImportSource @emotion/react */
import { css, jsx } from "@emotion/react";
import React, { useCallback } from "react";
import { useMessaging } from "@footron/controls-client";
import { Slider } from "@material-ui/core";

const containerStyle = css`
  padding: 16px;
  overflow-x: hidden;

  p {
    margin: 0 0 16px;
  }
`;

const ControlsComponent = (): jsx.JSX.Element => {
  const { sendMessage } = useMessaging<number>();

  const updateSlider = useCallback(
    async (event, value) => {
      await sendMessage(value);
    },
    [sendMessage]
  );

  return (
    <div css={containerStyle}>
      <p>
        <b>Move the slider to change the speed!</b>
      </p>
      <Slider
        min={0}
        max={1}
        onChange={updateSlider}
        step={0.05}
        marks
        defaultValue={0}
      />
    </div>
  );
};

export default ControlsComponent;
