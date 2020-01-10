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
        <el-row class="chart-container" align="center">
            <el-col :span="24">
                <div id="chartLine" style="width:100%; height:300px;"></div>
            </el-col>
<!--            <el-col :span="24">-->
<!--                <a href="http://echarts.baidu.com/examples.html" target="_blank" style="float: right;">more>></a>-->
<!--            </el-col>-->
        </el-row>
        <el-table :data="bugDayList" highlight-current-row v-loading="listLoading"  style="width: 100%;" align="center">
            <el-table-column prop="days" label="日期" width="200"></el-table-column>
            <el-table-column prop="everyday_bug" label="创建缺陷总数" width="200"></el-table-column>
            <el-table-column prop="everyday_resolved" label="修复缺陷总数" width="200"></el-table-column>
            <el-table-column prop="everyday_closed" label="关闭缺陷总数" width="200"></el-table-column>
        </el-table>
    </section>
</template>

<script>
    import { statisticBug } from "../../api/api.js";
    import util from "../../common/js/util";
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
                chartLine: null,
                listLoading:false,
                bugDayList:[],
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
            search() {
                this.statisticBug();
            },
            statisticBug() {
                let bugParams = {
                    startDate: this.filters.startDate ? util.formatDate.format(new Date(this.filters.startDate), 'yyyy-MM-dd') : '',
                    endDate: this.filters.endDate ? util.formatDate.format(new Date(this.filters.endDate), 'yyyy-MM-dd') : '',
                }
                statisticBug(bugParams).then((res) => {
                    this.daysList = res.daysList;
                    this.everyday_Bug = res.everyday_Bug;
                    this.everyday_resolved = res.everyday_resolved;
                    this.everyday_closed = res.everyday_closed;
                    this.drawLineChart(res.daysList, res.everyday_Bug, res.everyday_resolved, res.everyday_closed);
                    this.bugDayList =  res.bugDayList;
                    this.listLoading = false;
                });
            },

            drawLineChart(daysList, everyday_Bug, everyday_resolved, everyday_closed) {
                this.chartLine = echarts.init(document.getElementById('chartLine'));
                this.chartLine.setOption({
                    title: {
                        text: '缺陷日趋势图'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['创建缺陷总数', '修复缺陷总数', '关闭缺陷总数']
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        axisLabel:{
                            interval:0,
                            rotate:30
                        },
                        data: daysList
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            name: '创建缺陷总数',
                            type: 'line',
                            stack: '总量',
                            data: everyday_Bug
                        },
                        {
                            name: '修复缺陷总数',
                            type: 'line',
                            data: everyday_resolved
                        },
                        {
                            name: '关闭缺陷总数',
                            type: 'line',
                            data: everyday_closed
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
