<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateVolumebotTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('volumebot', function (Blueprint $table) {
            $table->increments('id');
            $table->date('start_date');
            $table->time('timefrom');
            $table->time('timeto')->nullable();            
            $table->float('volume',16,8);            
            $table->string('status');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('volumebot');
    }
}
