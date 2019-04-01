function put_semi_circle_graph(container_id,graph_title,series_data,measure,colors_args) {
	//var str = JSON.stringify(embed_dict, null, 2);
	// alert(series_data);
	// Highcharts.setOptions({
    //     colors:['#2ECCFA', '#FF0000', '#672F6C', '#FF8000', '#E65F00' ,'#40FF00']
    //    });

	Highcharts.chart(container_id, {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    // colors: ['#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce',
    // '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a'],
    title: {
        text: graph_title,
        align: 'center',
        verticalAlign: 'middle',
        y: 50
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b> <br><b>{point.y:.0f} '+measure+'</b>'
    },
    plotOptions: {
        pie: {
            colors: colors_args ,
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
					color: 'white'
                }
                ,
                formatter: function() {
                    if (this.y != 0) {
                      return this.point.name;
                    } else {
                      return null;
                    }
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '90%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Porcentaje',
        innerSize: '50%',
        data: series_data
    }]
});
}




