function put_semi_circle_graph(container_id,graph_title,series_data) {
	//var str = JSON.stringify(embed_dict, null, 2);
	// alert(series_data);
	
	Highcharts.chart(container_id, {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: graph_title,
        align: 'center',
        verticalAlign: 'middle',
        y: 50
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b> <br><b>{point.y:.0f} Mensajes</b>'
    },
    plotOptions: {
        pie: {
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




