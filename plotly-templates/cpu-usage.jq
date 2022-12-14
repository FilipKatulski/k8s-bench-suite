{
    "data": [
        {
            "meta": {
                "columnNames": {
                    "x": "scenario",
                    "y": "client"
                }
            },
            "name": "client",
            "type": "bar",
            "x": [
                if .data.idle? then "Idle" else empty end,
                if .data.pod2pod.tcp? then "pod2pod-tcp" else empty end,
                if .data.pod2pod.udp? then "pod2pod-udp" else empty end,
                if .data.pod2pod.custom? then "pod2pod-custom" else empty end,
                if .data.pod2svc.tcp? then "pod2svc-tcp" else empty end,
                if .data.pod2svc.udp? then "pod2svc-udp" else empty end,
                if .data.pod2svc.custom? then "pod2svc-custom" else empty end
            ],
            "y": [
                if .data.idle? then .data.idle.client.cpu.total else empty end,
                if .data.pod2pod.tcp? then .data.pod2pod.tcp.client.cpu.total else empty end,
                if .data.pod2pod.udp? then .data.pod2pod.udp.client.cpu.total else empty end,
                if .data.pod2pod.custom? then .data.pod2pod.custom.client.cpu.total else empty end,
                if .data.pod2svc.tcp? then .data.pod2svc.tcp.client.cpu.total else empty end,
                if .data.pod2svc.udp? then .data.pod2svc.udp.client.cpu.total else empty end,
                if .data.pod2svc.custom? then .data.pod2svc.custom.client.cpu.total else empty end
            ],
            "marker": {
                "color": "rgb(31, 119, 180)"
            },
            "text": [
                if .data.idle? then .data.idle.client.cpu.total else empty end,
                if .data.pod2pod.tcp? then .data.pod2pod.tcp.client.cpu.total else empty end,
                if .data.pod2pod.udp? then .data.pod2pod.udp.client.cpu.total else empty end,
                if .data.pod2pod.custom? then .data.pod2pod.custom.client.cpu.total else empty end,
                if .data.pod2svc.tcp? then .data.pod2svc.tcp.client.cpu.total else empty end,
                if .data.pod2svc.udp? then .data.pod2svc.udp.client.cpu.total else empty end,
                if .data.pod2svc.custom? then .data.pod2svc.custom.client.cpu.total else empty end
            ],
            "showlegend": true,
            "legendgroup": 1,
            "textposition": "inside"
        },
        {
            "meta": {
                "columnNames": {
                    "x": "scenario",
                    "y": "server"
                }
            },
            "name": "server",
            "type": "bar",
            "x": [
                if .data.idle? then "Idle" else empty end,
                if .data.pod2pod.tcp? then "pod2pod-tcp" else empty end,
                if .data.pod2pod.udp? then "pod2pod-udp" else empty end,
                if .data.pod2pod.custom? then "pod2pod-custom" else empty end,
                if .data.pod2svc.tcp? then "pod2svc-tcp" else empty end,
                if .data.pod2svc.udp? then "pod2svc-udp" else empty end,
                if .data.pod2svc.custom? then "pod2svc-custom" else empty end
            ],
            "y": [
                if .data.idle? then .data.idle.server.cpu.total else empty end,
                if .data.pod2pod.tcp? then .data.pod2pod.tcp.server.cpu.total else empty end,
                if .data.pod2pod.udp? then .data.pod2pod.udp.server.cpu.total else empty end,
                if .data.pod2pod.custom? then .data.pod2pod.custom.server.cpu.total else empty end,
                if .data.pod2svc.tcp? then .data.pod2svc.tcp.server.cpu.total else empty end,
                if .data.pod2svc.udp? then .data.pod2svc.udp.server.cpu.total else empty end,
                if .data.pod2svc.custom? then .data.pod2svc.custom.server.cpu.total else empty end
            ],
            "yaxis": "y",
            "marker": {
                "color": "rgb(214, 39, 40)"
            },
            "text": [
                if .data.idle? then .data.idle.server.cpu.total else empty end,
                if .data.pod2pod.tcp? then .data.pod2pod.tcp.server.cpu.total else empty end,
                if .data.pod2pod.udp? then .data.pod2pod.udp.server.cpu.total else empty end,
                if .data.pod2pod.custom? then .data.pod2pod.custom.server.cpu.total else empty end,
                if .data.pod2svc.tcp? then .data.pod2svc.tcp.server.cpu.total else empty end,
                if .data.pod2svc.udp? then .data.pod2svc.udp.server.cpu.total else empty end,
                if .data.pod2svc.custom? then .data.pod2svc.custom.server.cpu.total else empty end
            ],
            "showlegend": true,
            "legendgroup": 1,
            "textposition": "inside"
        }
    ],
    "layout": {
        "font": {
            "size": 12,
            "color": "rgb(33, 33, 33)",
            "family": "\"Droid Serif\", serif"
        },
        "title": {
            "text": "CPU usage"
        },
        "xaxis": {
            "tickfont": {
                "size": 14,
                "family": "Droid Serif"
            },
            "tickangle": -45
        },
        "yaxis": {
            "tickfont": {
                "size": 14,
                "family": "Droid Serif"
            }
        },
        "barmode": "group",
        "boxmode": "overlay"
    }
}
