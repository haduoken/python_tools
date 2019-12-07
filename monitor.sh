#!/bin/bash

node_list=(
"/camera_node"
"/imu_link_slam_link" 
"/joy"
"/kilox_global_plan"
"/kilox_joy_controller"
"/kilox_modbus_tcp_fast_node"
"/kilox_modbus_tcp_node"
"/kilox_navigation_show_node"
"/kilox_robot_manager"
"/map_odom"
"/map_rs_odom"
"/map_server_2d"
"/obstacle_detection_node"
"/robot_link_to_rslidar"
"/robot_manager_py"
"/robot_state_publisher"
"/rosapi"
"/rosbridge_websocket"
"/rosout"
"/rs_gps"
"/rs_localization_ros"
"/rscloud_node"
"/rslidar_node"
"/test_local_plan_node"
"/tf2_web_republisher"
)
echo -e "-----------------------------------------------------------------------------------------------------------------"
date | awk '{print $1" "$2" "$3" "$4" "$5}'
cpu_info="cpu:"`sar -u 1 1 | awk 'NR==4 {print $3}'`"%    "
memory_raw=`sar -r 1 1 | awk 'NR==4 {print $2"/"$4}'`
memory_info="kbmemfree:"${memory_raw%/*}"    memusage:"${memory_raw#*/}"%    "
used_disk=`df -h /usr | awk 'NR==2 {print $5"    "}'`
num_used_disk=${used_disk%\%*}
if [[ $((${num_used_disk})) > 90 ]]; then
	`rm -r ~/.ros/log/*`
fi
disk_info="diskused:"`df -h /usr | awk 'NR==2 {print $3"    "}'`"availdisk:"`df -h /usr | awk 'NR==2 {print $4"    "}'`"diskusage:"`df -h /usr | awk 'NR==2 {print $5"    "}'`
echo -e ${cpu_info}${memory_info}${disk_info}
sar -n DEV 1 1 | awk 'NR==7||NR==8||NR==9 {print $0}'
echo "Disconnet node :"
node_num=${#node_list[@]}
for (( i = 0; i < ${node_num}; i++ )); do
	query=`rosnode list | grep ${node_list[i]}`
	if [[ ${query} == "" ]]; then
		echo -e ${node_list[i]}
	fi
done
