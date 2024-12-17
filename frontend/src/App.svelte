<script>
  import { onMount } from "svelte";
  import videojs from "video.js";
  import "video.js/dist/video-js.css";

  let player;
  let videos = [];
  let selectedVideo = null;
  let isVideoReady = false;

  onMount(async () => {
    const res = await fetch("/api/list_videos");
    const data = await res.json();
    videos = data.videos;
  });

  const playVideo = async () => {
    const res = await fetch("/api/generate_hls", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_name: selectedVideo }),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.message === "First chunk ready!") {
        isVideoReady = true;
        initializeVideoPlayer();
      }
    }
  };

  const initializeVideoPlayer = () => {
    if (player) {
      player.dispose();
    }
    player = videojs("videoPlayer", {}, function () {
      console.log("Video.js player initialized!");
    });
  };
</script>

<div
  class="flex flex-col bg-gray-900 rounded-lg shadow-lg text-gray-100 h-max w-screen p-4"
>
  <div
    class="max-w-4xl mx-auto p-6 bg-gray-700 rounded shadow-lg text-gray-100"
  >
    <h1 class="text-3xl font-bold mb-6 text-center">CCTV Viewer</h1>

    <div class="grid grid-cols-3 gap-6">
      <div
        class="bg-gradient-to-b from-gray-900 to-gray-800 p-5 rounded-lg shadow-xl h-48 hover:scale-105 transform transition duration-300"
      >
        <h2 class="text-xl font-bold text-white mb-3">Recent Alerts</h2>
        <p class="text-gray-400 text-base">
          Stay updated with the latest alerts or notifications.
        </p>
        <button
          class="mt-4 px-4 py-2 bg-indigo-500 text-white rounded-lg shadow-md hover:bg-indigo-600"
        >
          View Alerts
        </button>
      </div>

      <div
        class="bg-gradient-to-b from-gray-900 to-gray-800 p-5 rounded-lg shadow-xl h-48 hover:scale-105 transform transition duration-300"
      >
        <h2 class="text-xl font-bold text-white mb-3">CCTV Status</h2>
        <p class="text-gray-400 text-base">
          Monitor live feeds or review camera settings.
        </p>
        <button
          class="mt-4 px-4 py-2 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600"
        >
          View CCTV
        </button>
      </div>

      <div
        class="bg-gradient-to-b from-gray-900 to-gray-800 p-5 rounded-lg shadow-xl h-48 hover:scale-105 transform transition duration-300"
      >
        <h2 class="text-xl font-bold text-white mb-3">Summary</h2>
        <p class="text-gray-400 text-base">
          Review daily and weekly activity summaries.
        </p>
        <button
          class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600"
        >
          View Summary
        </button>
      </div>
    </div>

    <!-- Video Player Section -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4 text-center">Video Player</h2>
      <div class="mb-6">
        <label for="videoSelect" class="block text-lg font-semibold mb-2"
          >Select a Video:</label
        >
        <select
          id="videoSelect"
          class="bg-gray-800 text-gray-200 border border-gray-600 rounded w-full p-3"
          bind:value={selectedVideo}
        >
          <option disabled value="">-- Choose a video --</option>
          {#each videos as video}
            <option value={video}>{video}</option>
          {/each}
        </select>
      </div>

      <button
        class="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 text-lg font-semibold rounded disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={!selectedVideo}
        on:click={playVideo}
      >
        Play Video
      </button>

      {#if isVideoReady}
        <div class="mt-8">
          <h2 class="text-lg font-bold mb-4">Now Playing:</h2>
          <div class="aspect-video bg-black rounded shadow-lg overflow-hidden">
            <video
              class="video-js vjs-default-skin w-full h-full"
              id="videoPlayer"
              controls
              autoplay
              preload="auto"
            >
              <source src="/hls/output.m3u8" type="application/x-mpegURL" />
              <track
                src=""
                kind="captions"
                srclang="en"
                label="English Captions"
              />
            </video>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <div class="flex-shrink-0 bg-gray-700 p-4 rounded-md text-center mt-4">
    <p class="text-sm text-gray-400">© CCTV Dashboard</p>
  </div>
</div>
