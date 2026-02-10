import { app } from "../../scripts/app.js";

const TARGET_NODE_TYPES = [
    "EagleFeederPng",
    "EagleFeederAnimatedWebp",
    "EagleFeederMp4",
];

app.registerExtension({
    name: "comfyui-eagle-feeder.defaults",

    nodeCreated(node) {
        if (!TARGET_NODE_TYPES.includes(node.comfyClass)) {
            return;
        }

        const widget = node.widgets?.find((w) => w.name === "file_server_host");
        if (widget && widget.value === "localhost") {
            const hostname = window.location.hostname;
            if (hostname && hostname !== "" && hostname !== "localhost") {
                widget.value = hostname;
            }
        }
    },
});
