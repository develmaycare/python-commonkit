class STAGE:
    """Standardized stages of a project or product."""
    PLANNING = "planning"
    EXPERIMENTAL = "experimental"
    DEVELOPMENT = "development"
    ALPHA = "alpha"
    BETA = "beta"
    RELEASE = "release"
    LIVE = "live"
    OBSOLETE = "obsolete"

    COLORS = {
        PLANNING: "lightgray",
        EXPERIMENTAL: "red",
        DEVELOPMENT: "blue",
        ALPHA: "orange",
        BETA: "yellow",
        RELEASE: "yellowgreen",
        LIVE: "green",
        OBSOLETE: "000000",
    }

    ORDERING = [
        PLANNING,
        EXPERIMENTAL,
        DEVELOPMENT,
        ALPHA,
        BETA,
        RELEASE,
        LIVE,
        OBSOLETE,
    ]

    VERSION_IDENTIFIERS = {
        PLANNING: "p",
        EXPERIMENTAL: "x",
        DEVELOPMENT: "d",
        ALPHA: "a",
        BETA: "b",
        RELEASE: "r",
        LIVE: "",
        OBSOLETE: "o",
    }
