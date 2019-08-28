<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateBotplansTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('botplans', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->date('start_date');
            $table->time('timefrom');
            $table->time('timeto');
            $table->integer('side')->default(0);
            $table->float('volume',16,8);
            $table->float('startprice',16,8);
            $table->string('status');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('botplans');
    }
}
