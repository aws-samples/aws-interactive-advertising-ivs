/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

// ----------------------------------------------------------------------------------------

/*
 * AWS SDK command:
 * aws ivs put-metadata --channel-arn CHANNEL_ARN --metadata METADATA

 
 * Product:
 * "{\"type\": \"product\",\"image\": \"https://m.media-amazon.com/images/I/81YdmTK0CLL._AC_SX750_.jpg\",\"title\": \"Short Sleeve T-Shirt\",\"description\": \"Solids: 100% Cotton; Heathers: 60% Cotton, 40% Polyester. Everyday made better: we listen to customer feedback and fine-tune every detail to ensure quality, fit, and comfort \",\"price\": \"USD 10.99\"}"



 * Clear:
 * "{\"type\": \"clear\"}"
*/

// ----------------------------------------------------------------------------------------

const playbackUrl = "https://3789d4f99cba.eu-west-1.playback.live-video.net/api/video/v1/eu-west-1.524894586859.channel.7JgSJtPFObtm.m3u8";

// ----------------------------------------------------------------------------------------
const videoPlayer = document.getElementById("video-player");
const interactivityOverlay = document.getElementById("interactivity-overlay");

const appEl = document.getElementById("app");
const playerEl = document.getElementById("player");
const playerOverlay = document.getElementById("player-overlay");
const playerControls = document.getElementById("player-controls");
const btnMute = document.getElementById("mute");
const btnFullscreen = document.getElementById("fullscreen");



const productEl = document.getElementById("product");
const productImageEl = document.getElementById("product__img");
const productQrEl = document.getElementById("product__qr");
const productTitleEl = document.getElementById("product__title");
const productPriceEl = document.getElementById("product__price");
const productDescriptionEl = document.getElementById("product__description");



(function (IVSPlayer) {
  const PlayerState = IVSPlayer.PlayerState;
  const PlayerEventType = IVSPlayer.PlayerEventType;

  // Initialize player
  const player = IVSPlayer.create();
  player.attachHTMLVideoElement(videoPlayer);

  // Timed Metadata event listener
  player.addEventListener(PlayerEventType.TEXT_METADATA_CUE, function (cue) {
    const metadataText = cue.text;
    console.log(`${metadataText}`);
    triggerOverlay(metadataText);
  });

  // Setup stream and play
  player.setAutoplay(true);
  player.load(playbackUrl);

  // Setvolume
  player.setVolume(1);

  // Overlays
  // ----------------------------------------------------------------------------------------

 

  
  // {
  // "type": "product",
  // "image": "https://m.media-amazon.com/images/I/81YdmTK0CLL._AC_SX750_.jpg",
  // "qr": "https://url_of_qr"
  // "title": "",
  // "description": "",
  // "price": "USD 10.99"
  // }
  let showProduct = (metadata) => {
    productEl.classList.remove("hidden");
    productEl.classList.add("opacity__in");

    productImageEl.src = metadata.image;
    productQrEl.src = metadata.qr;
    productTitleEl.textContent = metadata.title;
    productDescriptionEl.textContent = metadata.description;
    productPriceEl.textContent = metadata.price;
  };

  let clearProduct = (metadata) => {
    productEl.classList.remove("opacity__in");
    productEl.classList.add("hidden");
    productImageEl.src = "";
    productQrEl.src = "";
    productTitleEl.textContent = "";
    productDescriptionEl.textContent = "";
    productPriceEl.textContent = "";
  };

  
  // -----------------

  let showDefault = (metadata) => {
    return false;
  };

  let clearDefault = (metadata) => {
    // TBA
  };

  // -----------------

  let clearAll = () => {

    clearProduct();
   
  };

  // -----------------

  let triggerOverlay = (metadata) => {
    clearAll();

    if (metadata) {
      try {
        let obj = JSON.parse(metadata);
        switch (obj.type) {
          case "quiz":
            showQuiz(obj);
            break;
          case "product":
            showProduct(obj);
            break;
          case "notice":
            showNotice(obj);
            break;
          case "clear":
            clearAll();
            break;
          default:
            showDefault(obj);
        }
      } catch (e) {
        console.log(e);
      }
    }
  };

  // Player controls
  // ----------------------------------------------------------------------------------------
  // Show/Hide player controls
  playerOverlay.addEventListener(
    "mouseover",
    (e) => {
      playerOverlay.classList.add("player--hover");
    },
    false
  );
  playerOverlay.addEventListener("mouseout", (e) => {
    playerOverlay.classList.remove("player--hover");
  });

  let setBtnMute = function () {
    btnMute.classList.remove("btn--mute");
    btnMute.classList.add("btn--unmute");
  };

  let setBtnUnmute = function () {
    btnMute.classList.add("btn--mute");
    btnMute.classList.remove("btn--unmute");
  };

  // Mute/Unmute
  btnMute.addEventListener(
    "click",
    (e) => {
      if (btnMute.classList.contains("btn--mute")) {
        setBtnMute();
        player.setMuted(1);
      } else {
        setBtnUnmute();
        player.setMuted(0);
      }
    },
    false
  );

  // Toggle fullscreen
  btnFullscreen.addEventListener("click", (e) => {
    toggleFullscreen();
  });

  let toggleFullscreen = () => {
    if (!playerEl.classList.contains("fullscreen")) {
      if (playerEl.requestFullscreen) {
        playerEl.requestFullscreen();
      } else if (playerEl.webkitRequestFullscreen) {
        /* Safari */
        playerEl.webkitRequestFullscreen();
      } else if (playerEl.msRequestFullscreen) {
        /* IE11 */
        playerEl.msRequestFullscreen();
      }
      playerEl.classList.add("fullscreen");
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) {
        /* Safari */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        /* IE11 */
        document.msExitFullscreen();
      }
      playerEl.classList.remove("fullscreen");
    }
  };

  // Handle exiting full screen
  playerEl.addEventListener("fullscreenchange", exitHandler);
  playerEl.addEventListener("webkitfullscreenchange", exitHandler);
  playerEl.addEventListener("mozfullscreenchange", exitHandler);
  playerEl.addEventListener("MSFullscreenChange", exitHandler);

  function exitHandler() {
    if (
      !document.fullscreenElement &&
      !document.webkitIsFullScreen &&
      !document.mozFullScreen &&
      !document.msFullscreenElement
    ) {
      playerEl.classList.remove("fullscreen");
    }
  }
})(window.IVSPlayer);

 