function put_pie_char(container_id,graph_title,series_data) {
	//var str = JSON.stringify(embed_dict, null, 2);
	//alert(series_data);


	Highcharts.chart(container_id, {
		chart: {
			styledMode: true
		},
		title: {
			text: graph_title
		},
		series: [{
			marker: {
				enabled: false
			},
			name:null,
			type: 'pie',
			allowPointSelect: true,
			keys: ['name', 'y', 'selected', 'sliced'],
			data: series_data,
			showInLegend : false
		}]
	});

}