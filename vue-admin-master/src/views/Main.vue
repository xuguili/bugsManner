<template>
    <section  >
         <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
		    <el-form :inline="true" :model="filters">
                <el-form-item label="创建时间">
                        <el-date-picker v-model="filters.startDate" type="date" placeholder="开始日期"
                                        :options="startDateOption" @on-change="onStartDateChange">
                        </el-date-picker>
                        <el-date-picker v-model="filters.endDate" type="date" placeholder="结束日期"
                        :options="endDateOption" @on-change="onEndDateChange">
                        </el-date-picker>
                </el-form-item>
				<el-form-item>
					<el-button type="primary" size="medium" icon="el-icon-search" v-on:click="search">生成报表</el-button>
				</el-form-item>
			</el-form>
        </el-col>
        <el-row class="chart-container">
            <el-col :span="12">
                <a href="http://localhost:8080/#/reportForms/BugCreater">详情</a>
                <div id="chartColumn" style="width:100%; height:300px;"></div>
            </el-col>
            <el-col :span="12">
                <a href="http://localhost:8080/#/reportForms/BugHandler">详情</a>
                <div id="chartBar" style="width:100%; height:300px;"></div>
            </el-col>
            <el-col :span="12">
                <a href="http://localhost:8080/#/reportForms/BugTrend">详情</a>
                <div id="chartLine" style="width:100%; height:300px;"></div>
            </el-col>
            <el-col :span="12">
                <a href="http://localhost:8080/#/reportForms/BugStatus">详情</a>
                <div id="chartPie" style="width:100%; height:300px;"></div>
            </el-col>
<!--            <el-col :span="24">-->
<!--                <a href="http://echarts.baidu.com/examples.html" target="_blank" style="float: right;">more>></a>-->
<!--            </el-col>-->
        </el-row>
    </section>
</template>

<script>
    import { statisticBug } from "../api/api.js";
    import util from "../common/js/util";
    import echarts from 'echarts'

    export default {
        data() {
            return {
                filters:{
                    startDate:'',
                    endDate:''
                },
                startDateOption:{},
                endDateOption:{},
                chartColumn: null,
                chartBar: null,
                chartLine: null,
                chartPie: null,
                listLoading:false
            }
        },

        methods: {
             onStartDateChange(startDate, type) {
                 this.endDateOption = {
                     disabledDate(endDate) {
                         return endDate < new Date(startDate) || endDate > Date.now()
                         }
                     }
                 },

            onEndDateChange(endDate, type) {
                this.startDateOption = {
                    disabledDate(startDate) {
                        return startDate > new Date(endDate) || startDate > Date.now()
                         }
                     }
                 },
            search(){
				this.statisticBug();
			},
            statisticBug(){
				let bugParams = {
                    startDate:this.filters.startDate ? util.formatDate.format(new Date(this.filters.startDate), 'yyyy-MM-dd'):'',
                    endDate:this.filters.endDate ? util.formatDate.format(new Date(this.filters.endDate), 'yyyy-MM-dd'):'',
				}
				statisticBug(bugParams).then((res) => {
					this.creater_name = res.creater_name;
					this.creater_bug = res.creater_bug;
					this.handler_name = res.handler_name;
					this.handler_bug = res.handler_bug;
					this.bugs_date = res.bugs_date;
					this.bugs_count = res.bugs_count;
					this.hasBug_resolved = res.hasBug_resolved;
					this.hasBug_closed = res.hasBug_closed;
					this.status = res.status;
					this.status_count = res.status_count;
					this.drawColumnChart(res.creater_name,res.creater_bug);
					this.drawBarChart(res.handler_name,res.handler_bug);
					this.drawLineChart(res.bugs_date,res.bugs_count,res.hasBug_resolved,res.hasBug_closed);
					this.drawPieChart(res.status,res.status_count)
				});
			},

            drawColumnChart(creater_name,creater_bug) {
                this.chartColumn = echarts.init(document.getElementById('chartColumn'));
                this.chartColumn.setOption({
                  title: {
                      text: '缺陷创建人分布图',

                },


                  tooltip: {},
                  xAxis: {
                      data:creater_name
                  },
                  yAxis: {},
                  series: [{
                      name: '缺陷数',
                      type: 'bar',
                      data:creater_bug
                    }]
                });
            },
            drawBarChart(handler_name,handler_bug) {
                this.chartBar = echarts.init(document.getElementById('chartBar'));
                this.chartBar.setOption({
                    title: {
                        text: '缺陷处理人分布图',
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    // legend: {
                    //     data: ['上月','本月']
                    // },
                    // grid: {
                    //     left: '3%',
                    //     right: '4%',
                    //     bottom: '3%',
                    //     containLabel: true
                    // },
                    xAxis: {
                        type: 'value',
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data:handler_name
                    },
                    series: [
                        // {
                        //     name: '上月',
                        //     type: 'bar',
                        //     data: [10, 32, 14, 56]
                        // },
                        {
                            // name: '本月',
                            type: 'bar',
                            data:handler_bug
                        }
                    ]
                });
            },
            drawLineChart(bugs_date,bugs_count,hasBug_resolved,hasBug_closed) {
                this.chartLine = echarts.init(document.getElementById('chartLine'));
                this.chartLine.setOption({
                    title: {
                        text: '缺陷日趋势图',
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['创建缺陷总数', '修复缺陷总数', '关闭缺陷总数']
                    },
                    // grid: {
                    //     left: '3%',
                    //     right: '4%',
                    //     bottom: '3%',
                    //     containLabel: true
                    // },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        axisLabel:{
                            interval:0,
                            rotate:30
                        },
                        data:bugs_date
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            name: '创建缺陷总数',
                            type: 'line',
                            stack: '总量',
                            data: bugs_count
                        },
                        {
                            name: '修复缺陷总数',
                            type: 'line',
                            data: hasBug_resolved
                        },
                        {
                            name: '关闭缺陷总数',
                            type: 'line',
                            data: hasBug_closed
                        }
                    ]
                });
            },
            drawPieChart(status,status_count) {
                this.chartPie = echarts.init(document.getElementById('chartPie'));
                this.chartPie.setOption({
                    title: {
                        text: '缺陷状态分布图',
                        // subtext: '缺陷状态',
                        x: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        data: ['新', '接受/处理', '已解决', '已验证', '已关闭','挂起', '重新打开']
                    },
                    series: [
                        {
                            name: '状态',
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            data: [
                                { value: status_count[5], name: '接受/处理' },
                                { value: status_count[4], name: '挂起' },
                                { value: status_count[1], name: '已拒绝' },
                                { value: status_count[2], name: '已解决' },
                                { value: status_count[0], name: '已关闭' },
                                { value: status_count[3], name: '已验证' },
                                { value: status_count[6], name: '新' },
                                { value: status_count[7], name: '重新打开' }

                            ],
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                });
            }
        },

        mounted: function () {
            this.statisticBug();
        }
    }
</script>

<style scoped>
    .chart-container {
        width: 100%;
        height: 100%;
        float: left;
    }
    /*.chart div {
        height: 400px;
        float: left;
    }*/

    .el-col {
        padding: 30px 20px;
    }
</style>
