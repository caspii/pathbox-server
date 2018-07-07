#!/usr/bin/env bash
ssh root@46.101.193.105 "cd pathbox.co && git pull && service apache2 restart"
