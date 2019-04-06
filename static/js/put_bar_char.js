function put_bar_char(container_id,graph_title,x_axis_categories,series,colors_arg) {
	//var str = JSON.stringify(embed_dict, null, 2);
	//alert(series_data);
	Highcharts.chart(container_id, {
    chart: {
        type: 'column'
    },
    title: {
        text: graph_title
	},
	
    legend: {
		enabled: false,
		align: 'right',
		verticalAlign: 'middle'
	  },
    xAxis: {
        categories: x_axis_categories,
        crosshair: true
    },
    yAxis: {
		min: 0,
		labels:
		{
		enabled: false
		}
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0"></td>' +
            '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: series
});
}