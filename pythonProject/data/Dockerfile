# FROM alpine:latest
# WORKDIR /data
# # all these files are in the data folder
# # smth like this /data/<NAME_OF_THE_CSV_FILE>
# COPY equipment_cycle.csv ./
# COPY non_unique_user_equipment.csv ./
# COPY unique_user_equipment.csv ./
# COPY test.csv ./
# COPY user_cycle.csv ./
# VOLUME /data

FROM alpine:latest
WORKDIR /data
COPY equipment_cycle.csv .
COPY non_unique_user_equipment.csv .
COPY unique_user_equipment.csv .
COPY test.csv .
COPY user_cycle.csv .
CMD ["sh"]