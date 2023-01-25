#!/bin/bash
$@ &
echo "-17" > /proc/$!/oom_adj