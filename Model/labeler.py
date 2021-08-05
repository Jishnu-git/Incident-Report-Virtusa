def label(data : "DataFrame") -> list:
    labels = ["Critical" if (resTime > 1000 or failure > 0.5) else (
              "Warning" if (failure > 0.3) else "Stable"
            ) for resTime, failure in zip(data["Average Response Time"], data["Failure Rate"])]

    return labels