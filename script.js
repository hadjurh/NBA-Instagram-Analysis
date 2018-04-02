let diameter = 800,
    radius = diameter / 2,
    innerRadius = radius - 120;

let cluster = d3.cluster()
    .size([360, innerRadius]);

let line = d3.radialLine()
    .curve(d3.curveBundle.beta(0.85))
    .radius(function (d) {
        return d.y;
    })
    .angle(function (d) {
        return d.x / 180 * Math.PI;
    });

let svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .append("g")
    .attr("transform", "translate(" + radius + "," + radius + ")");

let link = svg.append("g").selectAll(".link"),
    node = svg.append("g").selectAll(".node");

const transitionDuration = 300;

let players = [];
let dataFlare = [];

const smallData = "database/all-stars_2018/";
const fullData = "database/network_players_gt46_games/";
const dataInput = fullData;

d3.csv(dataInput + "player_username_id_team.csv", (dataCSV) => {
    dataCSV.forEach((player) => {
        players.push({
            name: player.NAME,
            instaName: player.USERNAME,
            group: player.TEAM
        });
    });

    d3.text(dataInput + "adjacency_matrix.csv", (text) => {
        d3.csvParseRows(text).forEach((playerSource, indexPlayerSource) => {
            const currentPlayerSource = players[indexPlayerSource];
            let playerLink = {
                name: "nba." + currentPlayerSource.group + "." + currentPlayerSource.name,
                size: 1,
                imports: []
            };

            playerSource.forEach((isLink, indexPlayerTarget) => {
                if(isLink === "1") {
                    const currentPlayerTarget = players[indexPlayerTarget];
                    playerLink.imports.push("nba." + currentPlayerTarget.group + "." + currentPlayerTarget.name);
                }
            });
            dataFlare.push(playerLink);
        });

        let root = packageHierarchy(dataFlare)
            .sum(function(d) { return d.size; });

        cluster(root);

        link = link
            .data(packageImports(root.leaves()))
            .enter().append("path")
                .each((d) => { d.source = d[0], d.target = d[d.length - 1]; })
                .attr("class", "link")
            .attr("d", line);

        node = node
            .data(root.leaves())
            .enter().append("text")
            .attr("class", "node")
            .attr("dy", "0.31em")
            .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? "" : "rotate(180)"); })
            .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
            .text(function(d) { return d.data.key; })
            .on("mouseover", mouseovered)
            .on("mouseout", mouseouted);


    });
});

function mouseovered(d) {

    link.each(function (l) {
        const currentLink = d3.select(this);
        if(l.target === d) {
            currentLink
                .style("stroke", "green");
        } else if (l.source === d ) {
            currentLink
                .style("stroke", "red");
        } else {
            currentLink
                    .style("opacity", 0);
        }
    })
}

function mouseouted(d) {
    link
        .style("opacity", 1)
        .style("stroke", "steelblue");
}

function packageHierarchy(classes) {
    let map = {};

    function find(name, data) {
        let node = map[name], i;
        if (!node) {
            node = map[name] = data || {name: name, children: []};
            if (name.length) {
                node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
                node.parent.children.push(node);
                node.key = name.substring(i + 1);
            }
        }
        return node;
    }

    classes.forEach(function(d) {
        find(d.name, d);
    });

    return d3.hierarchy(map[""]);
}

function packageImports(nodes) {
    let map = {},
        imports = [];

    // Compute a map from name to node.
    nodes.forEach(function(d) {
        map[d.data.name] = d;
    });

    // For each import, construct a link from the source to target node.
    nodes.forEach(function(d) {
        if (d.data.imports) d.data.imports.forEach(function(i) {
            imports.push(map[d.data.name].path(map[i]));
        });
    });

    return imports;
}