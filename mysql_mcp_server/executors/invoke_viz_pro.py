# -*- coding:utf-8 -*-
import json
from typing import List, Literal

from mcp.types import TextContent

from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def excute_invoke_viz_pro(
    choice_chart_types: List[
        Literal[
            "line",
            "area",
            "bar",
            "column",
            "boxplot",
            "candlestick",
            "range_bar",
            "range_area",
            "heatmap",
            "treemap",
            "funnel",
            "multi_axis",
            "pie_donut",
            "radar",
            "radial_bar_circular_gauge",
            "synchronized_charts",
        ]
    ],
    theme_colors: List[str],
) -> List[TextContent]:
    """
    데이터 분석 결과를 시각화하기 위해 최적의 차트 유형을 추천하는 전문 도구입니다.
    '시각화 전문가'를 호출하여, 제공된 데이터 특성과 분석 목적에 맞는 차트를 제안합니다.
    사용자가 선택할 수 있는 다양한 차트 유형(예: 꺾은선, 막대, 파이 등)을 기반으로, 데이터의 패턴, 분포, 관계를 효과적으로 표현할 수 있는 옵션을 반환합니다.
    이를 통해 보고서나 대시보드에 삽입할 시각 자료 설계를 지원합니다.

    Args:
        choice_chart_types: 사용자가 고려 중인 차트 유형 목록. 가능한 값은 다음과 같습니다:
            - 'line': 꺾은선 차트 (시간 추이 분석에 적합)
            - 'area': 영역 차트 (누적 데이터 표현에 유용)
            - 'bar': 막대 차트 (범주 간 비교에 적합)
            - 'column': 세로 막대 차트 (수직 비교 강조)
            - 'boxplot': 상자 그림 (분포 및 이상치 분석)
            - 'candlestick': 캔들스틱 차트 (금융 데이터 시각화)
            - 'range_bar': 범위 막대 차트 (범위 데이터 비교)
            - 'range_area': 범위 영역 차트 (범위 내 변화 표현)
            - 'heatmap': 히트맵 차트 (밀도 및 상관관계 시각화)
            - 'treemap': 트리맵 차트 (계층적 데이터 표현)
            - 'funnel': 깔때기 차트 (프로세스 단계 분석)
            - 'multi_axis': 다중 축 차트 (복합 데이터 비교)
            - 'pie_donut': 파이/도넛 차트 (비율 시각화)
            - 'radar': 레이더 차트 (다변수 비교)
            - 'radial_bar_circular_gauge': 방사형 막대/원형 게이지 (목표 달성률 표현)
            - 'synchronized_charts': 동기화 차트 (다중 데이터 동시 분석)
        theme_colors: 차트 색상 팔레트. 최대 10개의 색상을 지정할 수 있습니다.(hex 형식)

    Returns:
        List[TextContent]: 추천된 차트 유형과 그에 대한 설명을 JSON 형식의 문자열로 포함한 TextContent 리스트.
                          각 항목은 선택된 차트가 데이터 시각화에 적합한 이유를 설명합니다.
    """
    try:
        logger.info(f"[invoke_viz_pro] choice charts: {choice_chart_types}")
        logger.info(f"[invoke_viz_pro] theme colors: {theme_colors}")

        def get_chart_guidelines(
            chart_type: Literal[
                "line",
                "area",
                "bar",
                "column",
                "boxplot",
                "candlestick",
                "range_bar",
                "range_area",
                "heatmap",
                "treemap",
                "funnel",
                "multi_axis",
                "pie_donut",
                "radar",
                "radial_bar_circular_gauge",
                "synchronized_charts",
            ],
        ) -> str:
            if chart_type == "line":
                return (
                    chart_type,
                    """var lineChart = new ApexCharts(document.querySelector("#lineChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'line' 
            },
            series: [{ name: '판매량', data: [30, 40, 35, 50, 49, 60] }],
            xaxis: { categories: ['1월', '2월', '3월', '4월', '5월', '6월'] }
        });""",
                )
            elif chart_type == "area":
                return (
                    chart_type,
                    """var areaChart = new ApexCharts(document.querySelector("#areaChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'area' 
            },
            series: [{ name: '방문자 수', data: [10, 41, 35, 51, 49, 62] }],
            xaxis: { categories: ['월', '화', '수', '목', '금', '토'] },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.7,
                    opacityTo: 0.2,
                    stops: [0, 90, 100]
                }
            }
        });""",
                )
            elif chart_type == "bar":
                return (
                    chart_type,
                    """var barChart = new ApexCharts(document.querySelector("#barChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'bar' 
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true
                }
            },
            series: [{ name: '매출 (백만원)', data: [44, 55, 57, 56, 61, 58] }],
            xaxis: { categories: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'] }
        });""",
                )
            elif chart_type == "column":
                return (
                    chart_type,
                    """var columnChart = new ApexCharts(document.querySelector("#columnChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'bar' 
            },
            plotOptions: { 
                bar: { 
                    horizontal: false,
                    borderRadius: 4,
                    columnWidth: '60%'
                } 
            },
            series: [{ name: '수익 (억원)', data: [76, 85, 101, 98, 87, 105] }],
            xaxis: { categories: ['2019', '2020', '2021', '2022', '2023', '2024'] }
        });""",
                )
            elif chart_type == "boxplot":
                return (
                    chart_type,
                    """var boxPlot = new ApexCharts(document.querySelector("#boxPlot"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'boxPlot' 
            },
            series: [{
                data: [
                    { x: '1월', y: [54, 66, 69, 75, 88] },
                    { x: '2월', y: [43, 65, 69, 76, 81] },
                    { x: '3월', y: [31, 39, 45, 51, 59] }
                ]
            }],
            plotOptions: {
                boxPlot: {
                    colors: {
                        upper: themeColors[0],
                        lower: themeColors[1]
                    }
                }
            }
        });""",
                )
            elif chart_type == "candlestick":
                return (
                    chart_type,
                    """var candlestick = new ApexCharts(document.querySelector("#candlestick"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'candlestick' 
            },
            series: [{
                data: [
                    { x: new Date('2023-01-01'), y: [6629.81, 6650.50, 6623.04, 6633.33] },
                    { x: new Date('2023-01-02'), y: [6632.01, 6643.29, 6620.00, 6630.11] },
                    { x: new Date('2023-01-03'), y: [6630.71, 6649.00, 6626.00, 6648.50] }
                ]
            }],
            plotOptions: {
                candlestick: {
                    colors: {
                        upward: themeColors[2],
                        downward: themeColors[4]
                    }
                }
            }
        });""",
                )
            elif chart_type == "range_bar":
                return (
                    chart_type,
                    """var rangeBarChart = new ApexCharts(document.querySelector("#rangeBarChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'rangeBar' 
            },
            series: [{
                data: [
                    { x: '팀 A', y: [1, 5] },
                    { x: '팀 B', y: [4, 6] },
                    { x: '팀 C', y: [5, 8] }
                ]
            }],
            plotOptions: { 
                bar: { 
                    horizontal: true,
                    borderRadius: 4
                } 
            }
        });""",
                )
            elif chart_type == "range_area":
                return (
                    chart_type,
                    """var rangeAreaChart = new ApexCharts(document.querySelector("#rangeAreaChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'rangeArea' 
            },
            series: [
                { name: '최저', data: [{ x: '1월', y: 20 }, { x: '2월', y: 25 }, { x: '3월', y: 22 }] },
                { name: '최고', data: [{ x: '1월', y: 30 }, { x: '2월', y: 35 }, { x: '3월', y: 32 }] }
            ],
            fill: {
                opacity: [0.5, 0.25]
            }
        });""",
                )
            elif chart_type == "heatmap":
                return (
                    chart_type,
                    """var heatMapChart = new ApexCharts(document.querySelector("#heatMapChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'heatmap' 
            },
            series: [
                { name: '지표1', data: [20, 30, 40, 50, 60] },
                { name: '지표2', data: [10, 20, 30, 40, 50] }
            ],
            xaxis: { categories: ['월', '화', '수', '목', '금'] },
            colors: [themeColors[0]],
            plotOptions: {
                heatmap: {
                    colorScale: {
                        ranges: [{
                            from: 0,
                            to: 20,
                            color: themeColors[1],
                            name: '낮음'
                        }, {
                            from: 21,
                            to: 40,
                            color: themeColors[3],
                            name: '중간'
                        }, {
                            from: 41,
                            to: 60,
                            color: themeColors[0],
                            name: '높음'
                        }]
                    }
                }
            }
        });""",
                )
            elif chart_type == "treemap":
                return (
                    chart_type,
                    """var treemapChart = new ApexCharts(document.querySelector("#treemapChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'treemap' 
            },
            series: [{
                data: [
                    { x: 'A', y: 218 }, { x: 'B', y: 149 }, { x: 'C', y: 184 },
                    { x: 'D', y: 135 }, { x: 'E', y: 96 }
                ]
            }],
            plotOptions: {
                treemap: {
                    enableShades: true,
                    shadeIntensity: 0.5,
                    distributed: true
                }
            }
        });""",
                )
            elif chart_type == "funnel":
                return (
                    chart_type,
                    """var funnelChart = new ApexCharts(document.querySelector("#funnelChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'bar',
                stacked: true 
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                    borderRadius: 4
                }
            },
            series: [{ 
                name: '판매 단계', 
                data: [1200, 900, 600, 300, 100].reverse() 
            }],
            xaxis: {
                categories: ['리드', '잠재고객', '기회', '제안', '판매'].reverse()
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val;
                }
            }
        });""",
                )
            elif chart_type == "multi_axis":
                return (
                    chart_type,
                    """var multiAxisChart = new ApexCharts(document.querySelector("#multiAxisChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'line'
            },
            series: [
                { name: '온도 (°C)', data: [20, 25, 22, 28], yaxis: 0 },
                { name: '강수량 (mm)', data: [10, 15, 5, 20], yaxis: 1 }
            ],
            stroke: {
                width: [3, 3],
                curve: 'smooth'
            },
            markers: {
                size: [4, 4],
                hover: {
                    sizeOffset: 3
                }
            },
            yaxis: [
                { 
                    title: { 
                        text: "온도 (°C)",
                        style: {
                            color: themeColors[0]
                        }
                    },
                    labels: {
                        style: {
                            colors: themeColors[0]
                        }
                    }
                },
                { 
                    opposite: true, 
                    title: { 
                        text: "강수량 (mm)",
                        style: {
                            color: themeColors[1]
                        }
                    },
                    labels: {
                        style: {
                            colors: themeColors[1]
                        }
                    }
                }
            ],
            xaxis: { categories: ['1월', '2월', '3월', '4월'] }
        });""",
                )
            elif chart_type == "pie_donut":
                return (
                    chart_type,
                    """var pieChart = new ApexCharts(document.querySelector("#pieChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'pie' 
            },
            series: [44, 55, 13, 33],
            labels: ['A 제품', 'B 제품', 'C 제품', 'D 제품'],
            legend: {
                position: 'bottom'
            },
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 300
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        });""",
                )
            elif chart_type == "radar":
                return (
                    chart_type,
                    """var radarChart = new ApexCharts(document.querySelector("#radarChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'radar' 
            },
            series: [{ name: '역량 점수', data: [80, 50, 30, 40, 100, 20] }],
            xaxis: { categories: ['1월', '2월', '3월', '4월', '5월', '6월'] },
            fill: {
                opacity: 0.4
            },
            markers: {
                size: 4
            }
        });""",
                )
            elif chart_type == "radial_bar_circular_gauge":
                return (
                    chart_type,
                    """var radialBarChart = new ApexCharts(document.querySelector("#radialBarChart"), {
            ...commonOptions,
            chart: { 
                ...commonOptions.chart,
                type: 'radialBar' 
            },
            series: [75, 60, 45],
            labels: ['A 부서', 'B 부서', 'C 부서'],
            plotOptions: {
                radialBar: {
                    dataLabels: {
                        name: {
                            fontSize: '14px',
                            fontWeight: 500,
                            color: '#666'
                        },
                        value: {
                            fontSize: '20px',
                            fontWeight: 700,
                            color: '#333',
                            formatter: function (val) {
                                return val + '%';
                            }
                        }
                    },
                    hollow: {
                        size: '35%'
                    },
                    track: {
                        background: '#f2f2f2'
                    }
                }
            }
        });""",
                )
            elif chart_type == "synchronized_charts":
                return (
                    chart_type,
                    """var syncChart1 = new ApexCharts(document.querySelector("#syncChart1"), {
            chart: { 
                height: 200, 
                type: 'line', 
                id: 'chart1',
                group: 'sync-charts',
                toolbar: {
                    show: false
                }
            },
            series: [{ name: '추세 지표', data: [10, 20, 30, 40, 50] }],
            xaxis: { categories: ['1월', '2월', '3월', '4월', '5월'] },
            colors: [themeColors[0]],
            stroke: {
                curve: 'smooth',
                width: 3
            },
            markers: {
                size: 4
            }
        });""",
                )

        response_data = {
            "success": True,
            "apexcharts_js_guidelines": {
                "theme_colors": theme_colors,
                "common_options": {
                    "chart": {"height": 300, "fontFamily": "Pretendard", "toolbar": {"show": False}},
                    "colors": theme_colors,
                    "stroke": {"curve": "smooth", "width": 2},
                    "grid": {"borderColor": "#f1f1f1", "row": {"colors": ["transparent", "transparent"]}},
                    "markers": {"size": 4, "colors": theme_colors, "strokeColors": "#fff", "strokeWidth": 2},
                    "tooltip": {"theme": "light", "marker": {"show": True}},
                },
                "chart_guidelines": [get_chart_guidelines(chart_type) for chart_type in choice_chart_types],
                "end_script": "["
                + ",".join(
                    c_type for c_type, _ in [get_chart_guidelines(chart_type) for chart_type in choice_chart_types]
                )
                + "].forEach(chart => chart.render());",
            },
        }
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
