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
            <el-col :span="12">
                <div id="chartPie" style="width:100%; height:300px;"></div>
            </el-col>
<!--            <el-col :span="24">-->
<!--                <a href="http://echarts.baidu.com/examples.html" target="_blank" style="float: right;">more>></a>-->
<!--            </el-col>-->
        </el-row>
        <el-table :data="statusList" highlight-current-row v-loading="listLoading"  style="width: 50%;" align="center">
            <el-table-column prop="status" label="状态" width="300"></el-table-column>
            <el-table-column prop="status_count" label="小计" width="300"></el-table-column>
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
                chartPie: null,
                listLoading:false,
                statusList:[],
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
					this.status = res.status;
					this.status_count = res.status_count;
					this.drawPieChart(res.status,res.status_count);
					this.statusList = res.statusList;
					this.listLoading = false;
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
